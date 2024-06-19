from numpy import pi
from ..abc.aboptics import (
    Light,
    LCPLight,
    RCPLight,
    SLight,
    PLight,
    np,
    FresnelCoeff,
    Layer,
    WspInst,
    WaveLengthRange,
    ReducedConductivity,
    Permittivity,
    LorentzParameters,
    LorentzOscillator,
    Literal,
    TransferElement,
    ExpTransferElement,
    interpolate,
)
from ..abc.abpshe import SubDat, SubstrateObj, OutDat, Union
from ..pubmeth.pubmeth import Line
import matplotlib.pyplot as plt


class IFShift:
    def __init__(self, wls, shift, light: Union[Light, str] = Light(1, 0)) -> None:
        self.wls = wls
        self.shift: np.ndarray = shift

        if isinstance(light, Light):
            self.label = light.__class__.__name__[:3]
        elif isinstance(light, str):
            self.label = light

    def __repr__(self) -> str:
        return np.array2string(self.shift)

    def __add__(self, shift2: Union["IFShift", float, int]) -> "IFShift":
        if isinstance(shift2, IFShift):
            return IFShift(self.wls, self.shift + shift2.shift, "PlusLight")
        else:
            return IFShift(self.wls, self.shift + shift2, "PlusScalar")

    def __radd__(self, shift2: Union["IFShift", float, int]) -> "IFShift":
        return self.__add__(shift2)

    def __sub__(self, shift2: Union["IFShift", float, int]) -> "IFShift":
        if isinstance(shift2, IFShift):
            return IFShift(self.wls, self.shift - shift2.shift, "DiffLight")
        else:
            return IFShift(self.wls, self.shift - shift2, "DiffScalar")

    def __rsub__(self, shift2: Union["IFShift", float, int]) -> "IFShift":
        if isinstance(shift2, IFShift):
            return IFShift(self.wls, shift2.shift - self.shift, "DiffLight")
        else:
            return IFShift(self.wls, shift2 - self.shift, "DiffScalar")

    def __len__(self):
        return len(self.shift)

    def plot(
        self,
        title: Literal["Thin-film model", "Conductivity model"] = "Thin-film model",
        suffix="",
    ):
        Line(self.wls, self.shift).plot(
            "{}_IF_{}{}".format(title, self.label, "_" + suffix),
            r"$\lambda$ (nm)",
            r"$\Delta_{IF}^{%s}$" % (self.label),
            title=title,
        )

    @property
    def center_y(self) -> float | int:
        return Line(self.wls, self.shift).center_of_curve()[1]

    @property
    def kb(self):
        return Line(self.wls, self.shift).kb_of_curve()


class GHShift(IFShift):
    def __init__(self, wls, shift, light: Light | str = Light(1, 0)) -> None:
        super().__init__(wls, shift, light)

    def plot(
        self,
        title: Literal["Thin-film model", "Conductivity model"] = "Thin-film model",
        suffix="",
    ):
        Line(self.wls, self.shift).plot(
            "{}_GH_{}{}".format(title, self.label, "_" + suffix),
            r"$\lambda$ (nm)",
            r"$\Delta_{GH}^{%s}$" % (self.label),
            title=title,
        )


class IFCalculation:
    def __init__(
        self,
        wlsInst: WaveLengthRange,
        light: Union[Literal["lcp", "rcp"], Light] = "lcp",
        theta0=np.pi / 4,
        subi=0,
        outi=0,
    ) -> None:
        self.wls_rangeInst = wlsInst
        if isinstance(light, str):
            self.light = eval("{}Light()".format(light.upper()))
        elif isinstance(light, Light):
            self.light = light
        self.theta0 = theta0
        self.subInst = SubDat()
        self.outInst = OutDat()

        self.subi = subi
        self.outi = outi

    def _rs_rp_cal(
        self,
        MatInst: Union[Permittivity, list[Permittivity], ReducedConductivity],
        theta_in,
    ):
        subObj: SubstrateObj = self.subInst.sub_list[self.subi]
        outObj: SubstrateObj = self.outInst.out_list[self.outi]

        f = FresnelCoeff(
            theta_in,
            Layer(
                0, self.wls_rangeInst.wls_arr, subObj.nfunc(self.wls_rangeInst.wls_arr)
            ),
            Layer(
                0, self.wls_rangeInst.wls_arr, outObj.nfunc(self.wls_rangeInst.wls_arr)
            ),
        )
        if isinstance(MatInst, Permittivity):
            layers = [
                Layer(
                    MatInst.thickness, self.wls_rangeInst.wls_arr, MatInst.RefractiveN
                )
            ]
            r_s = f.thin_film_model(layers, direction="s")
            r_p = f.thin_film_model(layers, direction="p")
        elif isinstance(MatInst, list) and isinstance(MatInst[0], Permittivity):
            layers = [Layer(ele.thickness, ele.wls, ele.RefractiveN) for ele in MatInst]
            r_s = f.thin_film_model(layers, direction="s")
            r_p = f.thin_film_model(layers, direction="p")
        elif isinstance(MatInst, ReducedConductivity):
            r_s = f.conductivity_model(MatInst.sigma_tilde, direction="s")
            r_p = f.conductivity_model(MatInst.sigma_tilde, direction="p")
        return r_s, r_p

    def calculate(
        self,
        MatInst: Union[Permittivity, list[Permittivity], ReducedConductivity],
    ) -> IFShift:
        r_s, r_p = self._rs_rp_cal(MatInst, theta_in=self.theta0)

        k0 = (
            2
            * np.pi
            * self.subInst.sub_list[self.subi].nfunc(self.wls_rangeInst.wls_arr)
            / self.wls_rangeInst.wls_arr
        )

        R_s = np.abs(r_s)  # Amplitude of rs and rp
        R_p = np.abs(r_p)  # Amplitude of rs and rp
        phi_s = np.angle(r_s)  # Angle of rs and rp
        phi_p = np.angle(r_p)  # Angle of rs and rp

        wspInst = WspInst(self.light, R_s, R_p)

        Delta_IF = (
            -1
            / (k0 * np.tan(self.theta0))
            * (
                (wspInst.Wp * self.light.a_s**2 + wspInst.Ws * self.light.a_p**2)
                / (self.light.a_p * self.light.a_s)
                * np.sin(self.light.eta)
                + 2
                * np.sqrt(wspInst.Ws * wspInst.Wp)
                * np.sin(self.light.eta - phi_p + phi_s)
            )
        )

        return IFShift(self.wls_rangeInst.wls_arr, Delta_IF, self.light)


class GHCalculation(IFCalculation):
    def __init__(
        self,
        wlsInst: WaveLengthRange,
        light: Light | Literal["s", "p"] = "s",
        theta0=np.pi / 4,
        subi=0,
        outi=0,
    ) -> None:
        super().__init__(wlsInst, light, theta0, subi, outi)

    @property
    def theta_arr(self):
        delta_theta = 0.2 / 180 * pi
        theta_arr = np.linspace(
            self.theta0 - delta_theta, self.theta0 + delta_theta, 50
        )
        return theta_arr

    def calculate(
        self,
        MatInst: Permittivity | list[Permittivity] | ReducedConductivity,
    ) -> GHShift:

        r_s0, r_p0 = self._rs_rp_cal(MatInst, theta_in=self.theta0)

        angle_s = []
        angle_p = []

        for ele_theta in self.theta_arr:
            r_s, r_p = self._rs_rp_cal(MatInst, theta_in=ele_theta)

            angle_s.append(np.angle(r_s))
            angle_p.append(np.angle(r_p))

        angle_s = np.array(angle_s)
        angle_p = np.array(angle_p)

        f_s_list = [
            interpolate.interp1d(
                self.theta_arr[:-1], np.diff(angle_s[:, i]) / np.diff(self.theta_arr)
            )
            for i in range(angle_s.shape[-1])
        ]
        f_p_list = [
            interpolate.interp1d(
                self.theta_arr[:-1], np.diff(angle_p[:, i]) / np.diff(self.theta_arr)
            )
            for i in range(angle_p.shape[-1])
        ]

        par_phis = np.array([ele_f(self.theta0) for ele_f in f_s_list])
        par_phip = np.array([ele_f(self.theta0) for ele_f in f_p_list])

        R_s = np.abs(r_s0)  # Amplitude of rs and rp
        R_p = np.abs(r_p0)  # Amplitude of rs and rp

        wspInst = WspInst(self.light, R_s, R_p)

        k0 = (
            2
            * np.pi
            * self.subInst.sub_list[self.subi].nfunc(self.wls_rangeInst.wls_arr)
            / self.wls_rangeInst.wls_arr
        )

        Delta_GH = 1 / k0 * (wspInst.Ws * par_phis + wspInst.Wp * par_phip)

        return GHShift(self.wls_rangeInst.wls_arr, Delta_GH, light=self.light)


class BGIF(IFCalculation):
    def __init__(
        self,
        wlsInst: WaveLengthRange,
        MatInst: Permittivity | ReducedConductivity,
        light: Light | Literal["lcp", "rcp"] = "lcp",
        theta0=np.pi / 4,
        subi=0,
        outi=0,
    ) -> None:
        super().__init__(wlsInst, light, theta0, subi, outi)
        self.MatInst = MatInst

    @property
    def _bg_mat(self) -> Permittivity | ReducedConductivity:
        if isinstance(self.MatInst, Permittivity):
            mat_in = Permittivity(
                self.wls_rangeInst.wls_arr,
                self.MatInst.perm_infty * np.ones((len(self.wls_rangeInst.wls_arr),)),
                self.MatInst.thickness,
            )
        elif isinstance(self.MatInst, ReducedConductivity):
            mat_in = ReducedConductivity(
                self.wls_rangeInst.wls_arr, np.zeros((len(self.wls_rangeInst.wls_arr),))
            )
        return mat_in

    @property
    def wls(self):
        return self.wls_rangeInst.wls_arr

    @property
    def bg_shift(self) -> IFShift:
        return self.calculate(self._bg_mat)

    @property
    def bg_if_center_y(self):
        return self.bg_shift.center_y

    @property
    def bg_if_kb(self):
        return self.bg_shift.kb


class BGGH(BGIF, GHCalculation):
    def __init__(
        self,
        wlsInst: WaveLengthRange,
        MatInst: Permittivity | ReducedConductivity,
        light: Light | Literal["s", "p"] = "s",
        theta0=np.pi / 4,
        subi=0,
        outi=0,
    ) -> None:
        super().__init__(wlsInst, MatInst, light, theta0, subi, outi)

    @property
    def bg_shift(self) -> GHShift:
        return super(BGIF, self).calculate(self._bg_mat)


def main():

    centers = [2100]
    amps = [1]
    gammas = [50]

    wlsInst = WaveLengthRange(500, 700, 100)
    lp = LorentzParameters(centers, amps, gammas)
    lo = LorentzOscillator(lp, wlsInst)
    # lo.plot()

    cond = ReducedConductivity.lorentzO(lo)

    perm = Permittivity.sigma2d_to_perm(15.6, cond, 0.65)
    # perm = Permittivity.lorentzO(15.6, lo, d=0.65)

    s = 'IFCalculation(wlsInst, "rcp").calculate(cond)'

    shift_cm = eval(s)
    print("good")
    shift_tfm = IFCalculation(wlsInst, "rcp").calculate(perm)

    # shift = BGGH(wlsInst, perm, "s").bg_shift
    # shift.plot(suffix="bg")

    # ghinst = GHCalculation(wlsInst, "p")
    # shift_ghs = ghinst.calculate(perm)
    # shift_ghs.plot()

    # ghinst = GHCalculation(wlsInst, "s")
    # shift_ghs = ghinst.calculate(perm)
    # shift_ghs.plot()

    shift_cm.plot("Conductivity model")
    shift_tfm.plot("Thin-film model")

    # fig, ax_1 = plt.subplots()
    # ax_1.plot(shift_cm.wls, shift_cm.shift, "-", label="Conductivity model")
    # ax_1.plot(shift_tfm.wls, shift_tfm.shift, "r--", label="Thin-film model")
    # ax_1.set_aspect("auto")
    # ax_1.set_xlabel("", fontsize=12)
    # ax_1.set_ylabel("", fontsize=12)
    # ax_1.set_title("", fontsize=14)
    # ax_1.set_xlim(ax_1.get_xlim())
    # ax_1.set_ylim(ax_1.get_ylim())
    # fig.savefig("comp.png", dpi=330, facecolor="w", bbox_inches="tight", pad_inches=0.1)
    # plt.close()

    # shift1 = IFCalculation(wls, RCPLight()).calculate(cond, subi=0)
    # shift2 = IFCalculation(wls, LCPLight()).calculate(cond, subi=0)
    # shift1.plot(title="Conductivity model")
    # shift2.plot(title="Conductivity model")
    # shift_diff = shift1 - shift2
    # shift_diff.plot()

    # centers = [2100]
    # amps = [5]
    # gammas = [50]
    # lp = LorentzParameters(centers, amps, gammas)
    # lo = LorentzOscillator(lp, wls)
    # perm = Permittivity.lorentzO(15.6, lo, d=0.65)
    # perm.plot_perm("lambda")
    # perm.plot_n()

    # shif1 = IFCalculation(wls, "rcp").calculate(perm)
    # shif1.plot("Thin-film model")
    # shif2 = IFCalculation(wls, "lcp").calculate(perm)
    # shif2.plot("Thin-film model")

    # a1 = np.array([1, 2, 3, 4])
    # a2 = np.array([4, 3, 2, 1])

    # e1 = TransferElement(a1)
    # e2 = TransferElement(a2)

    # e3 = ExpTransferElement(1j * a1)

    # m1 = np.array([[e1, 0], [0, e1]])
    # m2 = np.array([[e2, 0], [0, e2]])

    # h1 = e2 / e1
    # print(h1.arr)

    # b1 = TransferElement(a1)
    # b2 = TransferElement(a2)

    # # m2 = np.array([[2, b2], [b1, 2]]) / b2
    # # m3 = np.array([[1, b2], [b1, 2]])

    # # print(m1)
    # e1 = ExpTransferElement(a2)
    # c1 = ExpTransferElement(a2) * a1
    # print(c1.arr)

    # result = m1 @ m2 @ np.array([1, 0])
    # print(result)
    # print(result[-1] / result[0])

    pass


if __name__ == "__main__":
    main()
