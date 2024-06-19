from numpy.core.function_base import linspace as linspace
from ..hamiltonians.tb_h import (
    TightTBGHa,
    TightAAtTTGHa,
    TightABtTTGHa,
    TightAtATTGHa,
    TightAtBTTGHa,
)
import numpy as np

# import matplotlib.pyplot as plt
from ..pubmeth.consts import *
from ..hamiltonians.conti_h import ContiTBGHa, EffABtHa, EffAtAHa, EffAtBHa
from typing import Literal
from ..bands.bands_cal import BandsCal
from ..bands.bands_plot import BandsPlot
from ..raman.raman_cal import RamanCal
from ..raman.raman_plot import RamanPlot
from ..abc.abmoire import ABContiGraMoires, ABContiMoHa, ABTBHa
from ..pubmeth.pubmeth import Line
from ..superlattices.comm_stru import (
    CommTBGStru,
    CommAAtTTGStru,
    CommABtTTGStru,
    CommAtATTGStru,
    CommAtBTTGStru,
)
from ..superlattices.stru_plot import StruPlot
from ..jdos.jdos_cal import JdosCal
from ..jdos.jdos_plot import JdosPlot
from ..dos.dos_cal import DosCal
from ..dos.dos_plot import DosPlot
from ..absorption.absorption_cal import AbsorptionCal
from ..absorption.absorption_plot import AbsorptionPlot


class ContiTBG(ABContiGraMoires):
    def __init__(
        self,
        twist_angle: float,
        haInst: ABContiMoHa = ContiTBGHa,
        vFcoeff: float = 1,
        a0: float = 2.46,
        kshells: int = 7,
        w_inter=118,
    ) -> None:
        super().__init__(twist_angle, haInst, vFcoeff, a0, kshells, w_inter)
        self.mat_name = "Twisted Bilayer Graphene"

    def eigs_at_points(self, point: Literal["K_t", "K_b", "M", "Gamma"] = "M"):
        h: ABContiMoHa = self.hInst(self)

        eig_vals = np.linalg.eig(h.h(getattr(h, point)))[0]
        return np.real(eig_vals)

    def bands(
        self,
        path: list[Literal["K_t", "K_b", "M", "Gamma"]] = ["K_t", "K_b", "Gamma", "M"],
        suffix="",
        ylim=None,
        density=100,
        ticklabelsize=10,
        titlesize=14,
        fontsize=12,
        xfontsize=12,
        title_name=None,
    ):
        if title_name is None:
            bds_title = "Band structures of {:.2f}$\degree$ {}".format(
                self.twist_angle, self.mat_name
            )
        else:
            bds_title = title_name
        h: ABContiMoHa = self.hInst(self)

        bcals = BandsCal(h, path=path, suffix=suffix, p_density=density)
        bplot = BandsPlot(bcals, titlesize=titlesize, fontsize=fontsize)
        bplot.plot(
            title_name=bds_title,
            ylim=ylim,
            ticklabelsize=ticklabelsize,
            xfontsize=xfontsize,
        )

    def raman(
        self,
        density=70,
        calcores=3,
        ffolder="",
        update_eles=False,
        bds_num=5,
        disable_elet=False,
        gamma=100,
        plot_over_eop=False,
    ) -> RamanPlot:
        h: ABContiMoHa = self.hInst(self)
        rcals = RamanCal(
            h, density=density, cal_corenum=calcores, bds_num=bds_num, gamma=gamma
        )
        rplot = RamanPlot(rcals, ffolder=ffolder, disable_elet=disable_elet)

        if plot_over_eop:
            ri_overeop, e_range = rplot.raman_eop_plot()
            ri_overeop_sum = ri_overeop.sum(axis=1).sum(axis=1)
            ri_modules = abs(ri_overeop_sum) ** 2
            Line(
                [e_range] * 2, [np.real(ri_overeop_sum), np.imag(ri_overeop_sum)]
            ).multiplot(
                "realimag_overeop",
                ["real part", "imaginary part"],
                "E (meV)",
                "Raman intensity",
                "Raman over photon energy",
                xlim=[1200, 3000],
            )
            Line(e_range, ri_modules).plot(
                "ri_overeop",
                "E (meV)",
                "Raman intensity",
                "Raman over photon energy",
                xlim=[1200, 3000],
            )

        pexisted = rplot.rFileInst.existed()[0]
        if (not pexisted) or update_eles:
            rplot.plot(update_elet=update_eles)
        return rplot

    def jdos(
        self,
        density=70,
        broadening=1,
        vc_num=3,
        calcores=3,
        update_npy=False,
        cal_hint=False,
        e_range=np.linspace(100, 2500, 200),
        large_scal_cal=False,
    ):
        h: ABContiMoHa = self.hInst(self)

        jcals = JdosCal(
            h,
            density,
            broadening=broadening,
            cal_corenum=calcores,
            vc_num=vc_num,
            cal_hint=cal_hint,
            e_range=e_range,
            large_scale_cal=large_scal_cal,
        )
        jplot = JdosPlot(jcals, update_npy=update_npy)

        jplot.plot()
        return

    def dos(
        self,
        density=70,
        broadening=1,
        calcores=3,
        update_npy=False,
        cal_hint=False,
        e_range=np.linspace(-2500, 2500, 200),
        large_scal_cal=False,
        save_dos_npy=False,
    ):
        h: ABContiMoHa = self.hInst(self)

        dcals = DosCal(
            h,
            density,
            dos_broadening=broadening,
            cal_corenum=calcores,
            cal_hint=cal_hint,
            e_range=e_range,
            large_scale_cal=large_scal_cal,
        )
        dosplot = DosPlot(dcals, update_npy=update_npy, dos_save=save_dos_npy)

        return dosplot.plot()

    def absorption(
        self,
        density=70,
        calcores=3,
        e_range=np.linspace(800, 4000, 400),
        ffolder="",
        update_eles=False,
        bds_num=5,
        disable_elet=True,
        gamma=100,
        degeneracy=2,
        update_npy=False,
    ):
        h: ABContiMoHa = self.hInst(self)
        abcals = AbsorptionCal(
            h,
            density=density,
            cal_corenum=calcores,
            bds_num=bds_num,
            gamma=gamma,
            degeneracy_factor=degeneracy,
            e_range=e_range,
        )
        abplot = AbsorptionPlot(abcals, ffolder, disable_elet=disable_elet)

        pexisted = abplot.abFileInst.existed()[0]
        if (not pexisted) or update_eles:
            abplot.plot(update_elet=update_eles, update_npy=update_npy)

        return abplot


class EffABt(ContiTBG):
    def __init__(
        self,
        twist_angle: float,
        haInst: ABContiMoHa = EffABtHa,
        vFcoeff: float = 1,
        a0: float = 2.46,
        kshells: int = 7,
        w_inter=118,
        tperp_coeff=1,
    ) -> None:
        super().__init__(twist_angle, haInst, vFcoeff, a0, kshells, w_inter)
        self.tperp_coeff = tperp_coeff

        self.mat_name = "ABt-Twisted Trilayer Graphene"


class EffAtA(ContiTBG):
    def __init__(
        self,
        twist_angle: float,
        haInst: ABContiMoHa = EffAtAHa,
        vFcoeff: float = 1,
        a0: float = 2.46,
        kshells: int = 7,
        w_inter=118,
        tperp_coeff=1,
    ) -> None:
        super().__init__(twist_angle, haInst, vFcoeff, a0, kshells, w_inter)
        self.tperp_coeff = tperp_coeff

        self.mat_name = "AtA-Twisted Trilayer Graphene"


class EffAtB(ContiTBG):
    def __init__(
        self,
        twist_angle: float,
        haInst: ABContiMoHa = EffAtBHa,
        vFcoeff: float = 1,
        a0: float = 2.46,
        kshells: int = 7,
        w_inter=118,
        tperp_coeff=1,
    ) -> None:
        super().__init__(twist_angle, haInst, vFcoeff, a0, kshells, w_inter)
        self.tperp_coeff = tperp_coeff

        self.mat_name = "AtB-Twisted Trilayer Graphene"


class TightTBG(CommTBGStru, ContiTBG):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa = TightTBGHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)

        self.mat_name = "Twisted Bilayer Graphene"

    def structure(self):
        h: TightTBGHa = self.hInst(self)
        strup = StruPlot(h.moInst)
        strup.plot()
        return

    def absorption(
        self,
        density=70,
        calcores=3,
        e_range=np.linspace(800, 4000, 400),
        ffolder="",
        update_eles=False,
        bds_num=5,
        disable_elet=True,
        gamma=100,
        degeneracy=1,
        update_npy=False,
    ):
        return super().absorption(
            density,
            calcores,
            e_range,
            ffolder,
            update_eles,
            bds_num,
            disable_elet,
            gamma,
            degeneracy,
            update_npy,
        )


class TightAAtTTG(TightTBG, CommAAtTTGStru):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa = TightAAtTTGHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)
        self.mat_name = "AAt-TTG"


class TightAtATTG(TightTBG, CommAtATTGStru):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa = TightAtATTGHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)
        self.mat_name = "AtA-TTG"


class TightABtTTG(TightAAtTTG, CommABtTTGStru):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa = TightABtTTGHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)
        self.mat_name = "ABt-TTG"


class TightAtBTTG(TightTBG, CommAtBTTGStru):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa = TightAtBTTGHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)
        self.mat_name = "AtB-TTG"


def main():
    # tbg = TightTBG(3, 3).structure()
    EffABt(16.2, kshells=3).jdos(density=7, update_npy=True)

    pass
    # print(ttg.lindexes)
    # print(ttg.lindexes)

    # def h(self, k_arr):
    #     # r_arrs = self.equal_distarrs[self.minnorm_index]
    #     # equal_vppi = self.equal_vppi[self.minnorm_index]
    #     # equal_vpps = self.equal_vpps[self.minnorm_index]
    #     # equal_cos = self.equal_cos[self.minnorm_index]
    #     # print(np.argmin(nor))
    #     equal_cos = self.equal_cos.reshape((-1, len(self.moInst.expand_basis))).T
    #     equal_vppi = self.equal_vppi.reshape((-1, len(self.moInst.expand_basis))).T
    #     equal_vpps = self.equal_vpps.reshape((-1, len(self.moInst.expand_basis))).T
    #     phase_term: np.ndarray = np.exp(1j * k_arr @ self.equal_distarrs[:, :2].T)
    #     phase_term = phase_term.reshape(-1, len(self.moInst.expand_basis)).T
    #     h = phase_term * (
    #         equal_vppi * (1 - equal_cos**2) + equal_vpps * equal_cos**2
    #     )
    #     h = np.sum(h, axis=0)
    #     h = h.reshape((len(self.moInst.latwithin), len(self.moInst.latwithin)))
    #     row, col = np.diag_indices_from(h)
    #     h[row, col] = 0

    #     pass

    #     return h

    # ContiTBG(12).bands()
    # a = np.array([[1, 2, 3], [4, 5, 3], [5, 3, 4]])
    # b = np.array([[True, False, False], [False, True, True], [False, False, False]])
    # print(a[b])


if __name__ == "__main__":
    main()
