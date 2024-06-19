from ..pshe.shift import (
    GHCalculation,
    IFCalculation,
    BGGH,
    BGIF,
    IFShift,
    GHShift,
)
from ..abc.abpshe import (
    ExpDat,
    SubDat,
    OutDat,
    ExpIFShiftEle,
    ExpGHShiftEle,
    Line,
)
from ..abc.aboptics import (
    LorentzOscillator,
    LorentzParameters,
    Permittivity,
    ReducedConductivity,
    Literal,
    WaveLengthRange,
)
from ..filesop.filesave import FilesSave
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt


class LorentzFitExp:
    def __init__(
        self,
        perm_infty,
        thickness,
        theta0=np.pi / 4,
        subi=0,
        outi=0,
        if_dat_name: str = "IF_colle",
        gh_dat_name: str = "GH_colle",
        sub_name="SubN",
        out_name="OutN",
        fInst=FilesSave("PSHE/fitting"),
    ) -> None:
        self.perm_infty = perm_infty
        self.thickness = thickness

        self.theta0 = theta0
        self.subi = subi
        self.outi = outi

        self.exp_dat = ExpDat(if_dat_name=if_dat_name, gh_dat_name=gh_dat_name)
        self.out_dat = OutDat(out_name=out_name)
        self.sub_dat = SubDat(sub_name=sub_name)

        self.fInst = fInst

    def perm_construct(self, wlsInst, args):
        lo_len = len(args) // 3
        center = args[:lo_len]
        amp = args[lo_len : 2 * lo_len]
        gamma = args[2 * lo_len : 3 * lo_len]

        lp = LorentzParameters(center, amp, gamma)
        lo = LorentzOscillator(lp, wlsInst)

        cond = ReducedConductivity.lorentzO(lo)
        perm = Permittivity.sigma2d_to_perm(self.perm_infty, cond, self.thickness)

        return lo, perm

    def shift_func(
        self,
        wls_x,
        *args,
        shift_type: Literal["if", "gh"] = "if",
        lightp: Literal["rcp", "lcp", "s", "p"] = "lcp"
    ):
        """
        args: [centers, amps, gammas, shift]
        """
        args = list(args[0])
        wlsInst = WaveLengthRange(wls_x)
        lo, perm = self.perm_construct(wlsInst, args)

        calInst: IFCalculation | GHCalculation = eval(
            "{}Calculation(wlsInst=wlsInst,light=lightp,theta0=self.theta0,subi=self.subi,outi=self.outi)".format(
                shift_type.upper()
            )
        )

        return calInst.calculate(perm).shift + args[-1]

    # def fit_if_tfm(self, sample_i, lp: LorentzParameters) :
    #     sample_dat: ExpIFShiftEle = self.exp_dat.if_shifts_list[sample_i]

    #     wlsInst = WaveLengthRange(sample_dat.wls)

    #     lo, perm = self.perm_construct(wlsInst, lp.pars_set)

    #     lcp_shift = IFCalculation(
    #         wlsInst=wlsInst,
    #         light="lcp",
    #         theta0=self.theta0,
    #         subi=self.subi,
    #         outi=self.outi,
    #     ).calculate(perm)

    #     rcp_shift = IFCalculation(
    #         wlsInst=wlsInst,
    #         light="rcp",
    #         theta0=self.theta0,
    #         subi=self.subi,
    #         outi=self.outi,
    #     ).calculate(perm)

    #     rcp_bg_shift = BGIF(
    #         wlsInst=wlsInst,
    #         MatInst=perm,
    #         light="rcp",
    #         theta0=self.theta0,
    #         subi=self.subi,
    #         outi=self.outi,
    #     )

    #     lcp_bg_shift = BGIF(
    #         wlsInst=wlsInst,
    #         MatInst=perm,
    #         light="lcp",
    #         theta0=self.theta0,
    #         subi=self.subi,
    #         outi=self.outi,
    #     )

    #     sample_dat.lcp_shift = (
    #         sample_dat.lcp_shift / sample_dat.lcp_kb[0] * lcp_bg_shift.bg_if_kb[0]
    #     )
    #     sample_dat.lcp_shift = (
    #         sample_dat.lcp_shift - sample_dat.lcp_center_y + lcp_bg_shift.bg_if_center_y
    #     )

    #     sample_dat.rcp_shift = (
    #         sample_dat.rcp_shift / sample_dat.rcp_kb[0] * rcp_bg_shift.bg_if_kb[0]
    #     )
    #     sample_dat.rcp_shift = (
    #         sample_dat.rcp_shift - sample_dat.rcp_center_y + rcp_bg_shift.bg_if_center_y
    #     )

    #     Line(
    #         [sample_dat.wls, lcp_shift.wls],
    #         [sample_dat.lcp_shift, lcp_shift.shift],
    #     ).multiplot(
    #         "init_par_IFexp_lcp",
    #         ["Experiment", "Theoretical"],
    #         r"$\lambda$ (nm)",
    #         r"$\Delta_{IF}^{LCP}$",
    #         title="LCP IF shift",
    #     )
    #     Line(
    #         [sample_dat.wls, rcp_shift.wls],
    #         [sample_dat.rcp_shift, rcp_shift.shift],
    #     ).multiplot(
    #         "init_par_IFexp_rcp",
    #         ["Experiment", "Theoretical"],
    #         r"$\lambda$ (nm)",
    #         r"$\Delta_{IF}^{RCP}$",
    #         title="RCP IF shift",
    #     )

    #     popt = curve_fit(
    #         lambda x, *p0: self.shift_func(x, p0, lightp="lcp"),
    #         sample_dat.wls,
    #         sample_dat.lcp_shift,
    #         p0=lp.pars_set,
    #         bounds=lp.pars_bound,
    #         maxfev=50000,
    #     )[0]

    #     print(popt)

    #     lo, perm = self.perm_construct(wlsInst, popt)

    #     fitted_shift = IFCalculation(
    #         wlsInst=wlsInst,
    #         light="lcp",
    #         theta0=self.theta0,
    #         subi=self.subi,
    #         outi=self.outi,
    #     ).calculate(perm)

    #     Line(
    #         [sample_dat.wls, fitted_shift.wls],
    #         [sample_dat.lcp_shift, fitted_shift.shift],
    #     ).multiplot(
    #         "fitted_par_IFexp_lcp",
    #         ["Experiment", "Theoretical"],
    #         r"$\lambda$ (nm)",
    #         r"$\Delta_{IF}^{LCP}$",
    #         title="LCP IF shift",
    #     )

    def plot_exp(self):
        self.exp_dat.plot_if_data()
        self.exp_dat.plot_gh_data()

    def fit(
        self,
        sample_i,
        lp: LorentzParameters,
        shift_type: Literal["if", "gh"] = "if",
        lightp: Literal["rcp", "lcp", "s", "p"] = "rcp",
        update_fit=False,
        plot_fitted_cond=True,
        twin_lim=[0, 0.6],
    ):
        fname = "{}exp_{}_sample{}".format(shift_type, lightp, sample_i)
        fInst = self.fInst + "FitFiles"

        if getattr(self.exp_dat, "exist_{}_data".format(shift_type)):
            print("Existing experiment data, fitting...")
        else:
            print("No experiment data found")

        sample_list = getattr(self.exp_dat, "{}_shifts_list".format(shift_type))
        sample_dat: ExpIFShiftEle | ExpGHShiftEle = sample_list[sample_i]

        wlsInst = WaveLengthRange(sample_dat.wls)

        lo, perm = self.perm_construct(wlsInst, lp.pars_set)

        the_shift: IFShift | GHShift = eval(
            "{}Calculation(wlsInst=wlsInst,light=lightp,theta0=self.theta0,subi=self.subi,outi=self.outi,).calculate(perm)".format(
                shift_type.upper()
            )
        )

        # bg_shift = BGIF(
        #     wlsInst=wlsInst,
        #     MatInst=perm,
        #     light=lightp,
        #     theta0=self.theta0,
        #     subi=self.subi,
        #     outi=self.outi,
        # )

        bg_shift: BGIF | BGGH = eval(
            "BG{}(wlsInst=wlsInst,MatInst=perm,light=lightp,theta0=self.theta0,subi=self.subi,outi=self.outi,)".format(
                shift_type.upper()
            )
        )

        setattr(
            sample_dat,
            "{}_shift".format(lightp),
            getattr(sample_dat, "{}_shift".format(lightp))
            / getattr(sample_dat, "{}_kb".format(lightp))[0]
            * bg_shift.bg_if_kb[0],
        )
        setattr(
            sample_dat,
            "{}_shift".format(lightp),
            getattr(sample_dat, "{}_shift".format(lightp))
            - getattr(sample_dat, "{}_center_y".format(lightp))
            + bg_shift.bg_if_center_y,
        )

        Line(
            [getattr(sample_dat, "wls"), the_shift.wls],
            [getattr(sample_dat, "{}_shift".format(lightp)), the_shift.shift],
            self.fInst + "initpar",
        ).multiplot(
            "initpar_{}exp_{}_sample{}".format(shift_type, lightp, sample_i),
            ["Experiment", "Theoretical"],
            r"$\lambda$ (nm)",
            r"$\Delta_{%s}^{%s}$" % (shift_type.upper(), lightp.upper()),
            title="{}-{} shift (Sample {})".format(
                lightp.upper(), shift_type.upper(), sample_i
            ),
            linestyles=[".", "-"],
        )

        if fInst.exist_npy(fname) and (not update_fit):
            print("Fitting done before, generating figures")
            popt = fInst.load_npy(fname)
        else:
            print("Fitting...\n")
            print("Init parameters are: ")
            print(lp.pars_set)
            popt = curve_fit(
                lambda x, *p0: self.shift_func(
                    x, p0, lightp=lightp, shift_type=shift_type
                ),
                getattr(sample_dat, "wls"),
                getattr(sample_dat, "{}_shift".format(lightp)),
                p0=lp.pars_set,
                bounds=lp.pars_bound,
                maxfev=50000,
            )[0]
            fInst.save_npy(fname, popt)

        lo_len = len(popt) // 3

        print("Fitted parameters:")
        print("Centers: ", list(popt[:lo_len]))
        print("Amplitudes: ", list(popt[lo_len : 2 * lo_len]))
        print("Gamma: ", list(popt[2 * lo_len : 3 * lo_len]))
        print("Overall shift: ", popt[-1], "\n")

        lo, perm = self.perm_construct(wlsInst, popt)

        fitted_shift: IFShift | GHShift = eval(
            "{}Calculation(wlsInst=wlsInst,light=lightp,theta0=self.theta0,subi=self.subi,outi=self.outi,).calculate(perm)".format(
                shift_type.upper()
            )
        )

        ax, fig = Line(
            [getattr(sample_dat, "wls"), fitted_shift.wls],
            [getattr(sample_dat, "{}_shift".format(lightp)), fitted_shift.shift],
            self.fInst + "fittedpar",
        ).multiplot(
            "fittedpar_{}exp_{}_sample{}".format(shift_type, lightp, sample_i),
            ["Experiment", "Theoretical"],
            r"$\lambda$ (nm)",
            r"$\Delta_{%s}^{%s}$" % (shift_type.upper(), lightp.upper()),
            title="{}-{} shift (Sample {})".format(
                lightp.upper(), shift_type.upper(), sample_i
            ),
            linestyles=[".", "-"],
            ax_return=True,
        )

        if plot_fitted_cond:
            cond = self._plot_2d_cond(popt, wlsInst)
            cond.fInst = self.fInst + "Cond"
            cond.plot(fname)

            ex_lines = list(ax.get_lines())
            ax_twin = ax.twinx()
            add_line = ax_twin.plot(
                cond.wls,
                cond.real_part,
                "r--",
            )
            ax_twin.set_ylabel(r"$\mathrm{Re}[\tilde{\sigma}]$", color="r")
            ax_twin.spines["right"].set_color("red")
            ax_twin.set_ylim(twin_lim)
            line_list = ex_lines + add_line
            ax_twin.tick_params(axis="y", color="r")

            handles, labels = ax.get_legend_handles_labels()
            leg_list = labels + ["Fitted 2D conductivity"]
            ax.legend(line_list, leg_list)

            for ele_label in ax_twin.get_yticklabels():
                ele_label.set_color("red")
            self.fInst.save_fig(fig, fname)
            plt.close(fig)

        return popt

    def _plot_2d_cond(self, popt, wlsInst) -> ReducedConductivity:
        lo_len = len(popt) // 3

        centers = popt[:lo_len]
        amps = popt[lo_len : 2 * lo_len]
        gammas = popt[2 * lo_len : 3 * lo_len]

        lp = LorentzParameters(centers, amps, gammas)
        lo = LorentzOscillator(lp, wlsInst)

        return ReducedConductivity.lorentzO(lo)

    def comp_cond(
        self,
        fname,
        fname_list,
        wlsInst: WaveLengthRange = WaveLengthRange(500, 700),
        title="",
        legends=None,
    ):
        fInst = self.fInst + "FitFiles"
        cond_list = []

        if legends is None:
            legends = ["Sample {}".format(ele[-1]) for ele in fname_list]
        else:
            pass
        for ele_name in fname_list:
            popt = fInst.load_npy(ele_name)
            lo_len = len(popt) // 3

            centers = popt[:lo_len]
            amps = popt[lo_len : 2 * lo_len]
            gammas = popt[2 * lo_len : 3 * lo_len]
            lp = LorentzParameters(centers, amps, gammas)
            lo = LorentzOscillator(lp, wlsInst)
            cond = ReducedConductivity.lorentzO(lo)
            cond_list.append(cond.real_part)
        Line([wlsInst.wls_arr] * len(fname_list), cond_list, self.fInst).multiplot(
            fname,
            legends,
            xlabel=r"$\lambda$ (nm)",
            ylabel=r"$\mathrm{Re}[\tilde{\sigma}]$",
            title=title,
        )


def main():

    # wlsInst = WaveLengthRange(500, 700)
    # lp = LorentzParameters([2000], [0.5], [50])
    # lo = LorentzOscillator(lp, wlsInst)
    # cond = ReducedConductivity.lorentzO(lo)
    # perm = Permittivity.sigma2d_to_perm(15.6, cond, 0.65)

    # lp = LorentzParameters([2200], [0.5], [50])
    # lo = LorentzOscillator(lp, wlsInst)
    # cond = ReducedConductivity.lorentzO(lo)
    # perm2 = Permittivity.sigma2d_to_perm(15.6, cond, 0.65)

    # ghshift_s = GHCalculation(wlsInst, "s").calculate(perm)
    # ghshift_p = GHCalculation(wlsInst, "p").calculate(perm)

    # testshift_p = GHCalculation(wlsInst, "p").calculate([perm2, perm])
    # testshift_s = GHCalculation(wlsInst, "s").calculate([perm2, perm])

    # # ghshift = BGGH(wlsInst, perm).calculate(perm)
    # ghshift_s.plot("GH-s")
    # ghshift_p.plot("GH-p")

    # testshift_p.plot("GH-p-test")
    # testshift_s.plot("GH-s-test")

    # wlsInst = WaveLengthRange(400, 800)
    # lp = LorentzParameters(
    #     [1800, 1900, 2000, 2100], [0.3, 0.3, 0.3, 0.3], [50, 50, 50, 50]
    # )
    # lo = LorentzOscillator(lp, wlsInst)
    # lo.plot()
    lp = LorentzParameters(
        [
            1825.9742034223834,
            1875.2060782602973,
            1929.5850575646718,
            1976.429785797628,
            2086.455798630417,
            2176.2986522772508,
            2268.5445084234475,
            2402.87722433451,
        ],
        [
            0.5051608050534825,
            0.20000000000000004,
            0.5544960560275749,
            0.3711244844449047,
            0.45322987395570524,
            0.35748517088865626,
            0.4225113293747884,
            0.6586445253162231,
        ],
        [
            29.400467019873812,
            10.000000000000002,
            43.484925870525245,
            23.02968872333086,
            45.61049846071738,
            97.46330614895763,
            110.67848457626937,
            54.13900146331418,
        ],
        components="e_amp_gamma",
        gamma_bot=10,
        shift_span=100,
    )
    # LorentzFitExp(15.6, 0.65).plot_exp()
    # for ele in range(len(ExpDat().gh_shifts_list)):
    #     LorentzFitExp(15.6, 0.65).fit(ele, lp, lightp="p", shift_type="gh")

    # LorentzFitExp(15.6, 0.65).fit(
    #     4, lp, lightp="p", shift_type="gh", update_fit=False, twin_lim=[0, 1]
    # )

    # for ele in range(len(ExpDat().gh_shifts_list)):
    #     LorentzFitExp(15.6, 0.65).fit(
    #         ele, lp, lightp="rcp", shift_type="if", update_fit=False, twin_lim=[0, 0.5]
    #     )
    #     LorentzFitExp(15.6, 0.65).fit(
    #         ele, lp, lightp="lcp", shift_type="if", update_fit=False, twin_lim=[0, 0.5]
    #     )
    #     LorentzFitExp(15.6, 0.65).fit(
    #         ele, lp, lightp="s", shift_type="gh", update_fit=False, twin_lim=[0, 1]
    #     )
    #     LorentzFitExp(15.6, 0.65).fit(
    #         ele, lp, lightp="p", shift_type="gh", update_fit=False, twin_lim=[0, 1]
    #     )

    # fname_list = ["ghexp_p_sample{}".format(ele) for ele in [0, 1, 2, 4]]
    # LorentzFitExp(15.6, 0.65).comp_cond(
    #     "p_light_comp_exclude3", fname_list, title="P-light GH fitted conductivity"
    # )

    # fname_list = ["ghexp_s_sample{}".format(ele) for ele in [0, 1, 2, 4]]
    # LorentzFitExp(15.6, 0.65).comp_cond(
    #     "s_light_comp_exclude3", fname_list, title="S-light GH fitted conductivity"
    # )

    # fname_list = ["ifexp_lcp_sample{}".format(ele) for ele in [0, 1, 2, 3, 4]]
    # LorentzFitExp(15.6, 0.65).comp_cond(
    #     "lcp_light_comp", fname_list, title="LCP-light IF fitted conductivity"
    # )

    # fname_list = ["ifexp_rcp_sample{}".format(ele) for ele in [0, 1, 2, 3, 4]]
    # LorentzFitExp(15.6, 0.65).comp_cond(
    #     "rcp_light_comp", fname_list, title="RCP-light IF fitted conductivity"
    # )

    fname_list = [
        "ghexp_p_sample4",
        "ghexp_s_sample4",
        "ifexp_lcp_sample4",
        "ifexp_rcp_sample4",
    ]
    LorentzFitExp(15.6, 0.65).comp_cond(
        "cond_comp_sample4",
        fname_list,
        title="Fitted conductivity for sample 4",
        legends=["p", "s", "LCP", "RCP"],
    )

    pass


if __name__ == "__main__":
    main()
