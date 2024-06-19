from ..superlattices.TwistedGra import ContiTBG, EffABt

import numpy as np
from typing import NewType, Union
from ..filesop.filesave import FilesSave, os
from ..raman.raman_plot import RamanPlot, RamanFiles, plt
from ..pubmeth.pubmeth import Line, PubMethod
from typing import Literal

vFmod = NewType("vFmod", float)
tperpmod = NewType("tperpmod", float)


class RamanScan:
    def __init__(
        self,
        instList: list[ContiTBG | EffABt],
        twists_arr: np.ndarray,
        ffolder="",
        density=5,
        update_eles=False,
        bds_num=5,
        calcores=3,
        disable_elet=False,
        gamma=100,
    ) -> None:
        self.matInstList = instList
        self.twists = twists_arr

        self.gamma = gamma

        self.density = density
        self.bds_num = bds_num
        self.ffolder = ffolder

        self.updele = update_eles
        self.calcores = calcores
        self.disable_elet = disable_elet

        self._set_scandir()

    def _set_scandir(self):
        self.scandir = FilesSave("Raman/{}".format(self.ffolder))

    def scancal(self) -> list[RamanPlot]:
        rplots_list = []
        print(
            "Calculating from ",
            self.matInstList[0].twist_angle,
            " degree to ",
            self.matInstList[-1].twist_angle,
            " degree. Total number of points: ",
            len(self.matInstList),
        )
        for eleInst in self.matInstList:
            eleplot = eleInst.raman(
                ffolder=self.ffolder,
                density=self.density,
                update_eles=self.updele,
                bds_num=self.bds_num,
                calcores=self.calcores,
                disable_elet=self.disable_elet,
                gamma=self.gamma,
            )
            rplots_list.append(eleplot)
        return rplots_list

    def elesum_scan(self):
        rplots_list = self.scancal()

        allelets = []
        AM_list = []
        for elep in rplots_list:
            eletd = elep.rFileInst.elet_fdir
            allelets.append(eletd.load_npy(elep.rFileInst.allinfo_fname))
            AM = elep.rCalInst.haInst.moInst.areaM
            AM_list.append(AM)
        elets_sum: np.ndarray = (
            np.array(allelets).sum(axis=1) / np.array(AM_list)[:, np.newaxis]
        )
        fig, ax = plt.subplots(1, 2, figsize=(10, 4))
        for elei in range(elets_sum.shape[-1]):
            ax[0].plot(self.twists, np.real(elets_sum[:, elei]))
            ax[0].set_aspect("auto")
            ax[0].set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax[0].set_ylabel("Real part", fontsize=12)
            ax[0].set_title("", fontsize=14)
            ax[1].plot(self.twists, np.imag(elets_sum[:, elei]))
            ax[1].set_aspect("auto")
            ax[1].set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax[1].set_ylabel("Imaginary part", fontsize=12)
            ax[1].set_title("", fontsize=14)
        self.scandir.save_fig(fig, "eletsum")
        return

    def make_elesmv(self, vlim=1, clim=1, frames=20):
        explot = self.matInstList[-1].raman(
            ffolder=self.ffolder,
            density=self.density,
            update_eles=self.updele,
            bds_num=self.bds_num,
            calcores=self.calcores,
            disable_elet=True,
        )
        if not explot.rFileInst.existed()[1]:
            self.disable_elet = False
            rplots_list = self.scancal()
        else:
            self.disable_elet = True
            rplots_list = self.scancal()

        mop_mvdir = self.scandir + "Mop2"
        elet_mvdir = self.scandir + "elet"
        ediff_mvdir = self.scandir + "ediff"

        imag_evo = []
        real_evo = []
        imag_evo_contour = []
        real_evo_contour = []

        for ele_v in range(vlim):
            for ele_c in range(ele_v, clim):
                fname = RamanFiles.elefname.format(ele_v + 1, ele_c + 1)
                mopfigs = []
                elet_realfigs = []
                elet_imagfigs = []
                edifffigs = []

                eletediff_realfigs = []
                eletediff_imagfigs = []

                for eleplot in rplots_list:
                    Mop_dir, elet_dir, ediff_dir = eleplot.rFileInst.ramandir()
                    mopfigs.append(Mop_dir.fig_dir + fname + ".png")
                    elet_realfigs.append(elet_dir.fig_dir + fname + "_real" + ".png")
                    elet_imagfigs.append(elet_dir.fig_dir + fname + "_imag" + ".png")
                    edifffigs.append(ediff_dir.fig_dir + fname + ".png")

                    eletediff_realfigs.append(
                        elet_dir.fig_dir + "elet_ediff" + os.sep + fname + "_real.png"
                    )
                    eletediff_imagfigs.append(
                        elet_dir.fig_dir + "elet_ediff" + os.sep + fname + "_imag.png"
                    )

                    imag_evo.append(elet_dir.fig_dir + "rdist_sum_imag.png")
                    real_evo.append(elet_dir.fig_dir + "rdist_sum_real.png")

                mop_mvdir.save_movie(mopfigs, fname, frames=frames)
                elet_mvdir.save_movie(elet_realfigs, fname + "_real", frames=frames)
                elet_mvdir.save_movie(elet_imagfigs, fname + "_imag", frames=frames)
                ediff_mvdir.save_movie(edifffigs, fname, frames=frames)

                elet_mvdir.save_movie(
                    eletediff_imagfigs,
                    fname + "_imag",
                    frames=frames,
                    subfolder="eletediff",
                )
                elet_mvdir.save_movie(
                    eletediff_realfigs,
                    fname + "_real",
                    frames=frames,
                    subfolder="eletediff",
                )
        for eleplot in rplots_list:
            Mop_dir, elet_dir, ediff_dir = eleplot.rFileInst.ramandir()

            imag_evo.append(elet_dir.fig_dir + "rdist_sum_imag.png")
            real_evo.append(elet_dir.fig_dir + "rdist_sum_real.png")

            imag_evo_contour.append(
                elet_dir.load_fig_path("rdist_sum_imag.png", subfolder="elet_ediff")
            )
            real_evo_contour.append(
                elet_dir.load_fig_path("rdist_sum_real.png", subfolder="elet_ediff")
            )

        elet_mvdir.save_movie(real_evo, "real_evo", frames=frames)
        elet_mvdir.save_movie(imag_evo, "imag_evo", frames=frames)
        elet_mvdir.save_movie(real_evo_contour, "real_evo_contour", frames=frames)
        elet_mvdir.save_movie(imag_evo_contour, "imag_evo_contour", frames=frames)

        return

    def raman_arr(self, xlim=[10, 20]):
        rplots_list = self.scancal()
        fname = RamanFiles.allinfo_fname

        ri_list = []
        rireal = []
        riimag = []

        rireal_neg = []
        rireal_pos = []
        riimag_neg = []
        riimag_pos = []

        for eleplot in rplots_list:
            elet_dir = eleplot.rFileInst.elet_fdir

            rdist = elet_dir.load_npy(fname)

            AM = eleplot.rCalInst.haInst.moInst.areaM

            ri_list.append((np.abs(np.sum(rdist)) / (self.density**2 * AM)) ** 2)

            rireal.append(np.real(np.sum(rdist)) / (self.density**2 * AM))
            riimag.append(np.imag(np.sum(rdist)) / (self.density**2 * AM))

            realnegs = np.sum(np.real(rdist)[np.real(rdist) < 0])
            realposi = np.sum(np.real(rdist)[np.real(rdist) >= 0])

            imagnegs = np.sum(np.imag(rdist)[np.imag(rdist) < 0])
            imagposi = np.sum(np.imag(rdist)[np.imag(rdist) >= 0])

            rireal_neg.append(realnegs / (self.density**2 * AM))
            rireal_pos.append(realposi / (self.density**2 * AM))
            riimag_neg.append(imagnegs / (self.density**2 * AM))
            riimag_pos.append(imagposi / (self.density**2 * AM))

        Line(self.twists, ri_list, self.scandir).plot(
            "rarr",
            r"$\theta$ ($\degree$)",
            "Raman Intensity (a.u.)",
            xlim=xlim,
        )
        Line([self.twists] * 2, [rireal, riimag], self.scandir).multiplot(
            "rarrrealimag",
            ["Real part", "Imaginary part"],
            r"$\theta$ ($\degree$)",
            "Raman Intensity (a.u.)",
            xlim=xlim,
        )
        Line([self.twists] * 3, [ri_list, rireal, riimag], self.scandir).semilogy(
            "rarrlog",
            ["Total", "Real", "Imaginary"],
            r"$\theta$ ($\degree$)",
            "Raman Intensity (a.u.)",
            xlim=xlim,
        )
        Line([self.twists] * 2, [rireal_neg, rireal_pos], self.scandir).multiplot(
            "real_negpos",
            ["Negative part", "Positive part"],
            r"$\theta$ ($\degree$)",
            "Raman Intensity (a.u.)",
            xlim=xlim,
        )
        print(np.max(ri_list) / ri_list[-1])

        return ri_list

    def raman_arr_over_eop(self):
        return

    def jdos_scan(
        self,
        e_range: np.ndarray = np.linspace(100, 2500, 200),
        broadening=1,
        update_elejdos=False,
        update_totjdos=True,
        update_jdos_npy=False,
        scan_type: Literal["jdos", "jdosmop"] = "jdos",
        cut_data=None,
    ):
        rplots_list = self.scancal()
        jdos_list = []

        e_op = rplots_list[0].rCalInst.e_op
        e_ph = rplots_list[0].rCalInst.e_ph
        gamma = rplots_list[0].rCalInst.gamma

        fname = "{}_{}".format(scan_type, broadening)
        f2name = "{}_{}_E_{:.2f}".format(scan_type, broadening, e_op)

        if (
            self.scandir.exist_fig(fname)
            and self.scandir.exist_fig(f2name)
            and (not update_totjdos)
        ):
            print("Figure {}, {} already exists, jumping out...".format(fname, f2name))
            return

        for elep in rplots_list:
            elejdos: np.ndarray = (
                elep.jdos_plot(
                    e_range=e_range,
                    broadening=broadening,
                    update_elejdos=update_elejdos,
                    plot_type=scan_type,
                    update_npy=update_jdos_npy,
                )
                .sum(axis=1)
                .sum(axis=1)
            )

            AM = elep.rCalInst.haInst.moInst.areaM

            jdos_list.append(elejdos / (self.density**2 * AM))

        twistpickarr = self.twists >= 10
        twistpick = self.twists[twistpickarr]
        jdospick = np.array(jdos_list)[twistpickarr]

        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(
            jdospick, extent=(e_range[0], e_range[-1], twistpick[-1], twistpick[0])
        )
        ax.vlines(
            e_op,
            colors="r",
            linestyles="dashed",
            ymin=twistpick[0],
            ymax=twistpick[-1],
        )
        ax.set_aspect("auto")
        ax.set_xlabel("E (meV)")
        ax.set_ylabel(r"$\theta$ ($\degree$)")
        ax.set_title("JDOS Map")
        c_ax = PubMethod.add_right_cax(ax, 0.01, 0.01)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label(r"JDOS ($\mathrm{meV}^{-1} \cdot \mathrm{A}^{-2}$)")
        self.scandir.save_fig(fig, fname=fname, save_pdf=True, subfolder="jdos")
        plt.close(fig)

        if cut_data is None:
            cut_data = [
                e_op,
                e_op - e_ph,
                e_op + e_ph,
            ]
        for cuti, elecut in enumerate(cut_data):
            cutname = "jdos_cut_{}_{}".format(broadening, elecut)
            jdos_at_eop = jdospick[:, np.argmin(np.abs(e_range - elecut))]

            fig, ax = plt.subplots()
            ax.plot(twistpick, jdos_at_eop)
            ax.set_aspect("auto")
            ax.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax.set_ylabel(
                r"JDOS ($\mathrm{meV}^{-1} \cdot \mathrm{A}^{-2}$)", fontsize=12
            )
            ax.set_title("JDOS at E={:.2f} meV".format(elecut), fontsize=14)
            self.scandir.save_fig(fig, fname=cutname, subfolder="jdos/cut")
            plt.close()

    def elejdos_scan(
        self,
        e_cut: float = 2330,
        broadening=1,
        update_elejdosscan=True,
        scan_type: Literal["jdos", "jdosmop"] = "jdos",
    ):
        rplots_list = self.scancal()
        jdos_list = []
        e_range: np.ndarray = np.linspace(100, 5000, 200)

        cuti = np.argmin(np.abs(e_range - e_cut))

        e_op = rplots_list[0].rCalInst.e_op
        e_ph = rplots_list[0].rCalInst.e_ph
        gamma = rplots_list[0].rCalInst.gamma

        fname = "{}_{}".format(scan_type, broadening)
        f2name = "{}_{}_E_{:.2f}".format(scan_type, broadening, e_op)

        if (
            self.scandir.exist_fig(fname)
            and self.scandir.exist_fig(f2name)
            and (not update_elejdosscan)
        ):
            print("Figure {}, {} already exists, jumping out...".format(fname, f2name))
            return

        for elep in rplots_list:
            ele_jdos = elep.jdos_plot(
                e_range=e_range,
                broadening=broadening,
                update_elejdos=False,
                plot_type=scan_type,
            )[cuti]

            AM = elep.rCalInst.haInst.moInst.areaM

            jdos_list.append(ele_jdos / (self.density**2 * AM))

        jdos_arr = np.array(jdos_list)
        jdos_sumk: np.ndarray = jdos_arr.sum(axis=1)

        for elei in range(jdos_sumk.shape[-1]):
            elejdos = jdos_sumk[:, elei]

            vi = elei % self.bds_num + 1
            ci = elei // self.bds_num + 1

            ele_fname = rplots_list[0].rFileInst.elefname.format(vi, ci)

            fig, ax = plt.subplots()
            ax.plot(self.twists, elejdos)
            ax.set_aspect("auto")
            ax.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax.set_ylabel(
                r"JDOS ($\mathrm{meV}^{-1} \cdot \mathrm{A}^{-2}$)", fontsize=12
            )
            ax.set_title(r"$v_{} \to c_{}$".format(vi, ci), fontsize=14)
            self.scandir.save_fig(fig, fname=ele_fname, subfolder="jdos/elejdos")
            plt.close()

    def elet_ediff_scan(self, update_eles=False, levels=None, colors=None):
        if levels is None:
            levels = 20
        elif isinstance(levels, list) or isinstance(levels, np.ndarray):
            levels.sort()
        rplots_list = self.scancal()
        for ele_p in rplots_list:
            ele_p.ediff_plot(update_eles=update_eles, levels=levels, colors=colors)
        return
