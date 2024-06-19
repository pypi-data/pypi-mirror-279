# from calcores.filesop.filesave import os, np, FilesSave
from ..filesop.filesave import FilesSave
import numpy as np
from typing import Literal, Union

# from calcores.pubmeth.pubmeth import ExcelMethod, FilesSave, Line
from ..pubmeth.pubmeth import ExcelMethod, FilesSave, Line, UnitsConversion
from abc import abstractproperty
from scipy import interpolate
from functools import cached_property
from colorama import Back, Fore, Style

# from calcores.pubmeth.pubmeth import UnitsConversion
from ..pubmeth.consts import *

# from public.consts import *


class Layer:
    def __init__(self, thickness, wls, n) -> None:
        self.d = thickness
        self.wls = wls
        self.n = n


class TransferElement:
    def __init__(self, arr) -> None:
        self.arr = arr

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return TransferElement(self.arr + other.arr)
        elif isinstance(other, (float, int, np.ndarray)):
            return TransferElement(self.arr + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(
        self, factor: Union["TransferElement", float, int, np.ndarray]
    ) -> "TransferElement":
        if isinstance(factor, self.__class__):
            return TransferElement(self.arr * factor.arr)
        elif isinstance(factor, (float, int, np.ndarray)):
            return TransferElement(self.arr * factor)

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def __truediv__(self, factor: Union["TransferElement", float, int, np.ndarray]):
        if isinstance(factor, self.__class__):
            return TransferElement(self.arr / factor.arr)
        elif isinstance(factor, (float, int, np.ndarray)):
            return TransferElement(self.arr / factor)

    def __rtruediv__(self, factor: Union["TransferElement", float, int, np.ndarray]):
        if isinstance(factor, self.__class__):
            return TransferElement(factor.arr / self.arr)
        elif isinstance(factor, (float, int, np.ndarray)):
            return TransferElement(factor / self.arr)


class ExpTransferElement(TransferElement):
    def __init__(self, arr) -> None:
        self.arr = np.exp(arr)


class WaveLengthRange:
    """
    Put the wavelength range list or array you investigate into the args parameter.

    Or you can input the start and the end wavelength. The default points over the wavelength range is 300
    """

    def __init__(self, *args, wls_points=300) -> None:
        self._args = args
        if len(args) == 3:
            self._wls_start = args[0]
            self._wls_end = args[1]
            self.wls_points = args[2]
        if len(args) == 2:
            self._wls_start = args[0]
            self._wls_end = args[1]
            self.wls_points = wls_points
        elif len(args) and isinstance(args[0], (np.ndarray, list)) == 1:
            pass

    @property
    def wls_arr(self):
        if len(self._args) == 3 or len(self._args) == 2:
            return np.linspace(self._wls_start, self._wls_end, self.wls_points)
        elif len(self._args) == 1:
            return np.array(self._args[0])

    @property
    def e_arr(self):  # in meV
        return 1240 / self.wls_arr * 1000


class Light:
    def __init__(self, a_s, a_p, eta=0) -> None:
        self.a_s = a_s
        self.a_p = a_p
        self.eta = eta
        pass


class LCPLight(Light):
    def __init__(self, a_s=1, a_p=1, eta=np.pi / 2) -> None:
        super().__init__(a_s, a_p, eta)


class RCPLight(Light):
    def __init__(self, a_s=1, a_p=1, eta=-np.pi / 2) -> None:
        super().__init__(a_s, a_p, eta)


class SLight(Light):
    def __init__(self, a_s=1, a_p=0, eta=0) -> None:
        super().__init__(a_s, a_p, eta)


class PLight(Light):
    def __init__(self, a_s=0, a_p=1, eta=0) -> None:
        super().__init__(a_s, a_p, eta)


class WspInst:
    def __init__(self, light: Light, R_s, R_p) -> None:
        self.light = light
        self.R_s = R_s
        self.R_p = R_p
        pass

    @property
    def Ws(self):
        return (
            self.R_s**2
            * self.light.a_s**2
            / (self.R_s**2 * self.light.a_s**2 + self.R_p**2 * self.light.a_p**2)
        )

    @property
    def Wp(self):
        return (
            self.R_p**2
            * self.light.a_p**2
            / (self.R_s**2 * self.light.a_s**2 + self.R_p**2 * self.light.a_p**2)
        )


class FresnelCoeff:
    def __init__(self, theta0, Layer1: Layer, Layer2: Layer) -> None:
        self.theta0 = theta0
        self.layer1 = Layer1
        self.layer2 = Layer2
        self.n0_index = Layer1.n
        self.n2_index = Layer2.n
        pass

    @property
    def theta2(self):
        quotient = self.n0_index * np.sin(self.theta0) / self.n2_index + 0j
        result = np.arcsin(quotient)
        result = np.real(result) - 1j * np.abs(np.imag(result))

        return result  # np.arcsin(quotient)

    @property
    def r_s(self):
        # return -np.sin(self.theta0 - self.theta2) / np.sin(self.theta0 + self.theta2)
        return (
            self.n0_index * np.cos(self.theta0) - self.n2_index * np.cos(self.theta2)
        ) / (self.n0_index * np.cos(self.theta0) + self.n2_index * np.cos(self.theta2))

    @property
    def r_p(self):
        # return np.tan(self.theta0 - self.theta2) / np.tan(self.theta0 + self.theta2)
        return (
            self.n2_index * np.cos(self.theta0) - self.n0_index * np.cos(self.theta2)
        ) / (self.n2_index * np.cos(self.theta0) + self.n0_index * np.cos(self.theta2))

    @property
    def t_s(self):
        return (
            2
            * self.n0_index
            * np.cos(self.theta0)
            / (
                self.n0_index * np.cos(self.theta0)
                + self.n2_index * np.cos(self.theta2)
            )
        )

    @property
    def t_p(self):
        return (
            2
            * self.n0_index
            * np.cos(self.theta0)
            / (
                self.n2_index * np.cos(self.theta0)
                + self.n0_index * np.cos(self.theta2)
            )
        )

    @property
    def delta(self):
        delta = (
            2
            * np.pi
            * self.n2_index
            * self.layer2.d
            * np.cos(self.theta2)
            / self.layer2.wls
        )
        return delta

    @property
    def phase_mat(self):
        phase = ExpTransferElement(1j * self.delta)
        phase_c = ExpTransferElement(-1j * self.delta)
        mat = np.array([[phase_c, 0], [0, phase]])
        return mat

    def _bound_mat(self, direction: Literal["s", "p"] = "s"):
        r = getattr(self, "r_{}".format(direction))
        t = getattr(self, "t_{}".format(direction))
        r_ele = TransferElement(r)
        t_ele = TransferElement(t)
        mat = np.array([[1, r_ele], [r_ele, 1]]) / t_ele
        return mat

    def thin_film_model(self, layers: list[Layer], direction: Literal["s", "p"]):
        """
        Layer list should not contain the layers in the init function
        """
        theta = self.theta0

        mat = np.eye(2)

        if isinstance(layers, Layer):
            layerscopy = [self.layer1, layers, self.layer2]
        elif isinstance(layers, list):
            layerscopy = layers[:]
            layerscopy.insert(0, self.layer1)
            layerscopy.append(self.layer2)
        for li in range(len(layerscopy) - 1):
            f = FresnelCoeff(theta, layerscopy[li], layerscopy[li + 1])
            mat = mat @ f._bound_mat(direction) @ f.phase_mat
            theta = f.theta2
        fi_vec = mat @ np.array([1, 0])
        out_r: TransferElement = fi_vec[-1] / fi_vec[0]
        return out_r.arr

    def conductivity_model(
        self, rsigma: "ReducedConductivity", direction: Literal["s", "p"] = "s"
    ):
        if direction == "s":
            r = (
                self.n0_index * np.cos(self.theta0)
                - self.n2_index * np.cos(self.theta2)
                - rsigma
            ) / (
                self.n0_index * np.cos(self.theta0)
                + self.n2_index * np.cos(self.theta2)
                + rsigma
            )
        elif direction == "p":
            r = (
                self.n2_index / np.cos(self.theta2)
                - self.n0_index / np.cos(self.theta0)
                + rsigma
            ) / (
                self.n2_index / np.cos(self.theta2)
                + self.n0_index / np.cos(self.theta0)
                + rsigma
            )
        return r


class LorentzParameters:
    """
    Input the 'centers', 'amplitudes', 'broadenings' of different Lorentzian peaks into pars parameter.
    """

    def __init__(
        self,
        *pars,
        components: Literal["e_amp_gamma", "lambda_amp_gamma"] = "e_amp_gamma",
        center_span=25,
        gamma_bot=25,
        gamma_top=150,
        shift_span=10,
        init_overall_shift=0
    ) -> None:
        self.pars = pars
        self.component = components

        self.center_span = center_span

        self.gamma_bot = gamma_bot
        self.gamma_top = gamma_top

        self.shift_span = shift_span

        self.init_overall_shift = init_overall_shift

        if len(set([len(ele) for ele in self.pars])) != 1:
            raise Exception("Should contain equal length list")

    @property
    def center(self):
        if self.component == "e_amp_gamma":
            return np.array(self.pars[0])
        elif self.component == "lambda_amp_gamma":
            return 1240 / np.array(self.pars[0]) * 1000

    @property
    def amplitude(self):
        return np.array(self.pars[1])

    @property
    def gamma(self):
        return np.array(self.pars[2])

    @property
    def pars_set(self):
        return [*self.center, *self.amplitude, *self.gamma, self.init_overall_shift]

    @property
    def pars_bound(self):
        center_bot = [ele - self.center_span for ele in self.center]
        amp_bot = [0.2] * len(self.amplitude)
        gamma_bot = [self.gamma_bot] * len(self.gamma)

        center_top = [ele + self.center_span for ele in self.center]
        amp_top = [1] * len(self.amplitude)
        gamma_top = [self.gamma_top] * len(self.gamma)

        shift_bot = [-self.shift_span]
        shift_top = [self.shift_span]

        bot_bound = center_bot + amp_bot + gamma_bot + shift_bot
        top_bound = center_top + amp_top + gamma_top + shift_top

        return (bot_bound, top_bound)


class LorentzOscillator:
    def __init__(
        self,
        lo_pars: LorentzParameters,
        wlsInst: WaveLengthRange = WaveLengthRange(500, 700),
    ) -> None:
        self.lo_pars = lo_pars
        self.wlsInst = wlsInst

    @cached_property
    def amplitude(self) -> np.ndarray:
        amps = (
            self.lo_pars.amplitude
            * np.sqrt(self.lo_pars.gamma / self.lo_pars.center)
            * self.lo_pars.center
        )
        return amps

    @property
    def gamma(self) -> np.ndarray:
        return self.lo_pars.gamma

    @property
    def center(self) -> np.ndarray:
        return self.lo_pars.center

    @property
    def e_x(self) -> np.ndarray:
        return self.wlsInst.e_arr

    @property
    def wls_x(self) -> np.ndarray:
        return self.wlsInst.wls_arr

    @cached_property
    def complex_result(self):
        amp = np.kron(np.ones((1, len(self.e_x))), self.amplitude.reshape(-1, 1))
        gamma = np.kron(np.ones((1, len(self.e_x))), self.gamma.reshape(-1, 1))
        centers = np.kron(np.ones((1, len(self.e_x))), self.center.reshape(-1, 1))
        x = np.kron(np.ones((len(self.amplitude), 1)), self.e_x.reshape(1, -1))
        result = amp**2 / (centers**2 - x**2 - 1j * gamma * x)
        result = np.sum(result, axis=0)
        return result

    @property
    def real_part(self):
        return np.real(self.complex_result)

    @property
    def imag_part(self):
        return np.imag(self.complex_result)

    def plot(self):
        Line([self.e_x] * 2, [self.real_part, self.imag_part]).multiplot(
            "realimag_lorentz", ["Real part", "Imaginary part"], "E (meV)"
        )


class ReducedConductivity:
    def __init__(self, wls, sigma_tilde, fInst: FilesSave = FilesSave("Cond")) -> None:
        self.wls = wls
        self.sigma_tilde = sigma_tilde
        self.fInst = fInst

    @staticmethod
    def lorentzO(lo: "LorentzOscillator") -> "ReducedConductivity":
        return ReducedConductivity(lo.wls_x, lo.complex_result * (-1j))

    @property
    def real_part(self):
        return np.real(self.sigma_tilde)

    @property
    def imag_part(self):
        return np.imag(self.sigma_tilde)

    def plot(self, fname: None | str = "realimag_cond"):
        Line(
            [self.wls] * 2, [self.real_part, self.imag_part], fInst=self.fInst
        ).multiplot(
            fname,
            ["Real part", "Imaginary part"],
            r"$\lambda$ (nm)",
            r"$\tilde{\sigma}$",
        )
        return


class Permittivity:
    """
    If you want to construct permittivity through Lorentzian oscillators, use the static method 'LorentzO'.
    """

    def __init__(self, wls, perm, thickness=1, perm_infty=None) -> None:  #    d in nm
        self.wls = wls
        self.perm = perm
        self.thickness = thickness
        self.perm_infty = perm_infty

    @staticmethod
    def lorentzO(perm_infty, lo: LorentzOscillator, d=1) -> "Permittivity":
        """
        perm_infty: The high-frequency dielectric constant

        lo: the LorentzOscillator class

        d: the thickness of the material
        """
        permInst = Permittivity(lo.wls_x, perm_infty + lo.complex_result, d, perm_infty)
        return permInst

    @property
    def sigma2d(self):
        omega = UnitsConversion.wls2omega(self.wls)
        sigma2d = self.perm * omega * self.thickness / (c_speed * m2nm * 1j)
        return ReducedConductivity(self.wls, sigma2d)

    @cached_property
    def RefractiveN(self):
        return np.sqrt(self.perm)

    @property
    def real_part(self):
        return np.real(self.perm)

    @property
    def imag_part(self):
        return np.imag(self.perm)

    def plot_perm(self, perspective: Literal["e", "lambda"] = "e"):
        if perspective == "e":
            x = self.wls
        elif perspective == "lambda":
            x = 1240 / self.wls * 1000
        Line([x] * 2, [self.real_part, self.imag_part]).multiplot(
            "realimag_perm",
            ["Real part", "Imaginary part"],
            r"$\lambda$ (nm)",
            "Permittivity",
        )
        return

    @staticmethod
    def sigma2d_to_perm(perm_infty, cond: ReducedConductivity, thickness):
        omega = UnitsConversion.wls2omega(cond.wls)
        response_term = (
            1j * (cond.sigma_tilde * c_speed * m2nm) / (omega * thickness) + perm_infty
        )

        return Permittivity(cond.wls, response_term, thickness, perm_infty)

    def plot_n(self):
        Line(
            [self.wls] * 2, [np.real(self.RefractiveN), np.imag(self.RefractiveN)]
        ).multiplot(
            "realimag_n",
            ["Real part", "Imaginary part"],
            r"$\lambda$ (nm)",
            "Refractive index",
        )
        return


def main():
    centers = [2000]
    amps = [1]
    gammas = [5]

    wls = WaveLengthRange(500, 700, 1000)
    lp = LorentzParameters(centers, amps, gammas)
    lo = LorentzOscillator(lp, wls)

    cond = ReducedConductivity.lorentzO(lo)

    perm1 = Permittivity.lorentzO(15, lo, 0.65)
    perm2 = Permittivity.lorentzO(18, lo, 0.65)
    per_list = [perm1, perm2]


if __name__ == "__main__":
    main()
