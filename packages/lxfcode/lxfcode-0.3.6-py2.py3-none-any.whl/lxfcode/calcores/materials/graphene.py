from ..abc.abmoire import ABContiGraMoires, ABContiMoHa
from ..hamiltonians.tb_h import SLGHa
from ..bands.bands_cal import BandsCal
from ..bands.bands_plot import BandsPlot
from ..raman.raman_plot import RamanCal, RamanPlot
from typing import Literal


class SLGra(ABContiGraMoires):
    mat_name = "Single layer graphene"

    def __init__(
        self,
        haInst: ABContiMoHa = SLGHa,
        vFcoeff: float = 1,
        a0: float = 2.46,
    ) -> None:
        super().__init__(0, haInst=haInst, vFcoeff=vFcoeff, a0=a0)

    @property
    def renormed_BZ_K_side(self):
        return self.K0

    @property
    def epsilonM(self):
        return self.epsilonO

    @property
    def areaM(self):
        return self.areaO

    def bands(
        self,
        path: list[Literal["K_t", "K_b", "M", "Gamma"]] = ["K_t", "K_b", "Gamma", "M"],
        suffix="",
    ):
        bds_title = "Band structures of {} {}".format(self.mat_name, self.mat_name)
        h: ABContiMoHa = self.hInst(self)

        bcals = BandsCal(h, path=path, suffix=suffix)
        bplot = BandsPlot(bcals)
        bplot.plot(title_name=bds_title)

    def raman(
        self,
        density=70,
        calcores=3,
        ffolder="",
        update_eles=False,
        bds_num=5,
        disable_elet=False,
        gamma=100,
    ) -> RamanPlot:
        h: ABContiMoHa = self.hInst(self)
        rcals = RamanCal(
            h, density=density, cal_corenum=calcores, bds_num=bds_num, gamma=gamma
        )
        rplot = RamanPlot(rcals, ffolder=ffolder, disable_elet=disable_elet)

        r_intensity = rplot.plot(update_elet=update_eles)
        print(r_intensity / (density**2 * self.areaO) ** 2)
        return rplot


def main():
    # fig, ax = plt.subplots()
    # ax.scatter(a.atoms_rvec("1")[:, 0], a.atoms_rvec("1")[:, 1], marker=".", s=1)
    # ax.scatter(a.atoms_rvec("2")[:, 0], a.atoms_rvec("2")[:, 1], marker=".", s=1)
    # coeff_arr = np.array(
    #     [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [-0.5, -0.5]]
    # )
    # boundvecs = np.kron(coeff_arr[:, 0].reshape((-1, 1)), a.R1) + np.kron(
    #     coeff_arr[:, 1].reshape((-1, 1)), a.R2
    # )
    # # boundvecs = np.vstack([np.zeros((1, 2)), a.R1, a.R1 + a.R2, a.R2, np.zeros((1, 2))])
    # ax.plot(boundvecs[:, 0], boundvecs[:, 1], "r-", lw=1)
    # ax.set_aspect("equal")
    # ax.set_xlabel("", fontsize=12)
    # ax.set_ylabel("", fontsize=12)
    # ax.set_title("", fontsize=14)
    # ax.set_xlim(ax.get_xlim())
    # ax.set_ylim(ax.get_ylim())
    # ax.legend([])
    # fig.savefig("tmp.png", dpi=330, facecolor="w", bbox_inches="tight", pad_inches=0.1)
    # fig.savefig("tmp.pdf", dpi=330, facecolor="w", bbox_inches="tight", pad_inches=0.1)
    # plt.close()

    # fig, ax = plt.subplots()
    # ax.scatter(
    #     a.atoms_rvec("within")[:, 0], a.atoms_rvec("within")[:, 1], marker=".", s=1
    # )
    # coeff_arr = np.array(
    #     [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [-0.5, -0.5]]
    # )
    # boundvecs = np.kron(coeff_arr[:, 0].reshape((-1, 1)), a.R1) + np.kron(
    #     coeff_arr[:, 1].reshape((-1, 1)), a.R2
    # )
    # # boundvecs = np.vstack([np.zeros((1, 2)), a.R1, a.R1 + a.R2, a.R2, np.zeros((1, 2))])
    # ax.plot(boundvecs[:, 0], boundvecs[:, 1], "r-", lw=1)
    # ax.set_aspect("equal")
    # ax.set_xlabel("", fontsize=12)
    # ax.set_ylabel("", fontsize=12)
    # ax.set_title("", fontsize=14)
    # ax.set_xlim(ax.get_xlim())
    # ax.set_ylim(ax.get_ylim())
    # ax.legend([])
    # fig.savefig("tmp2.png", dpi=330, facecolor="w", bbox_inches="tight", pad_inches=0.1)
    # fig.savefig("tmp2.pdf", dpi=330, facecolor="w", bbox_inches="tight", pad_inches=0.1)
    # plt.close()
    pass


if __name__ == "__main__":
    main()
