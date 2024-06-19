from .absorption_cal import AbsorptionCal
import numpy as np
from ..filesop.filesave import FilesSave
import matplotlib.pyplot as plt
from ..pubmeth.pubmeth import PubMethod, DefinedFuncs
import os
from typing import Literal


plt.rc("font", family="Times New Roman")  # change the font of plot
plt.rcParams["mathtext.fontset"] = "stix"


class AbsorptionPlot:
    fontsize = 12
    titlesize = 14

    def __init__(
        self,
        abCalInst: AbsorptionCal,
        ffolder="",
        disable_elet=False,
        # disable_eleMop_plot=True,
        # disable_eleEdiff_plot=True,
    ) -> None:
        self.abCalInst = abCalInst
        self.abFileInst = AbsorptionFiles(self.abCalInst, ffolder)

        self.disable_elet = disable_elet
        # self.disable_eleMop_plot = disable_eleMop_plot
        # self.disable_eleEdiff_plot = disable_eleEdiff_plot
        pass

    def _plot_ele_ab(
        self,
        ab_dist: np.ndarray,  #   (kpoints, e_range) array
        k_arrs,
        bound_vecs,
        elet_dir,
    ):
        # rdist_reallim, rdist_imaglim = PubMethod.sym_limit(
        #     raman_dist, split_realimag=True
        # )
        abdist_max = np.real(np.max(ab_dist))
        abdist_min = np.real(np.min(ab_dist))
        fig, ax = plt.subplots(figsize=(7, 7))
        print("Shape: ", ab_dist.shape)

        for ele_col in range(ab_dist.shape[-1]):
            # vi = ele_col % self.abCalInst.bds_num + 1
            # ci = ele_col // self.abCalInst.bds_num + 1

            fname = self.abFileInst.elefname.format(ele_col + 1)
            title = r"$\theta = {:.2f}\degree$ $E = {:.2f}$ meV".format(
                self.abCalInst.haInst.moInst.twist_angle,
                self.abCalInst.e_range[ele_col],
            )

            PubMethod.cmap_scatters(
                k_arrs[:, 0],
                k_arrs[:, 1],
                np.real(ab_dist[:, ele_col]),
                bound_vecs,
                elet_dir,
                fname,
                title=title,
                # vmin=abdist_min,
                # vmax=abdist_max,
                clabel_name="Absorption (a.u.)",
                figax_in=(fig, ax),
                cmap="jet",
            )
            # if self.disable_eleMop_plot:
            #     PubMethod.cmap_scatters(
            #         k_arrs[:, 0],
            #         k_arrs[:, 1],
            #         Mop2[:, ele_col],
            #         bound_vecs,
            #         Mop_dir,
            #         fname,
            #         title=title,
            #         vmin=-mop2_lim,
            #         vmax=mop2_lim,
            #         figax_in=(fig, ax),
            #     )
            # if self.disable_eleEdiff_plot:
            # PubMethod.cmap_scatters(
            #     k_arrs[:, 0],
            #     k_arrs[:, 1],
            #     ediff[:, ele_col],
            #     bound_vecs,
            #     ediff_dir,
            #     fname,
            #     title=title,
            #     clabel_name=r"$\Delta E$",
            #     cmap="jet",
            #     figax_in=(fig, ax),
            # )
        plt.close(fig)

    def plot(self, update_elet=False, update_npy=False):
        elet_dir = self.abFileInst.abdir()
        (
            ab_dist,  #  (kpoints, e_range) array
            # Mop2,  #  (n*n) array
            # ediff,  #  (n*n) array
            k_arrs,
            bound_vecs,
            eleplots,
        ) = self.abFileInst.abload(update_npy=update_npy)

        if (not self.disable_elet) and (eleplots or update_elet):
            print("Plotting element transitions...")
            self._plot_ele_ab(
                ab_dist,
                # Mop2,
                # ediff,
                k_arrs,
                bound_vecs,
                # Mop_dir,
                elet_dir,
                # ediff_dir,
            )

        ab_intensity = np.sum(ab_dist, axis=0)

        fig, ax_ab = plt.subplots()
        ax_ab.plot(self.abCalInst.e_range, np.real(ab_intensity))
        ax_ab.set_aspect("auto")
        ax_ab.set_xlabel("E (meV)", fontsize=12)
        ax_ab.set_ylabel("Absorption", fontsize=12)
        ax_ab.set_title(
            r"$\theta={}\degree$".format(self.abCalInst.haInst.sigs), fontsize=14
        )
        ax_ab.set_xlim(ax_ab.get_xlim())
        ax_ab.set_ylim(ax_ab.get_ylim())
        elet_dir.save_fig(fig, "Absorption_over_e")
        plt.close(fig)

        return ab_dist

    # def jdos_plot(
    #     self,
    #     e_range=np.linspace(100, 2500, 200),
    #     broadening=1,
    #     update_elejdos=False,
    #     update_npy=False,
    #     plot_type: Literal["jdos", "jdosmop"] = "jdos",
    # ):
    #     jdos_dir = self.abFileInst.jdos_dir

    #     (
    #         raman_dist,
    #         Mop2,
    #         ediff,
    #         k_arrs,
    #         bound_vecs,
    #         eleplots,
    #     ) = self.abFileInst.abload()

    #     fname = "{}_{:.2f}".format(plot_type, broadening)
    #     if jdos_dir.exist_npy(fname) and (not update_npy):
    #         jdos = np.real(jdos_dir.load_npy(fname))
    #     else:
    #         jdos = DefinedFuncs.deltaF_arct(ediff, e_range, a=broadening)
    #         if plot_type == "jdos":
    #             jdos_dir.save_npy(fname, jdos)
    #         elif plot_type == "jdosmop":
    #             Mop_e: np.ndarray = np.kron(np.ones((jdos.shape[0], 1, 1)), Mop2)
    #             jdos = np.real(jdos * Mop_e)
    #             jdos_dir.save_npy(fname, np.real(jdos))
    #             print("Complete saving: ", fname)
    #     targ_i = np.argmin(abs(e_range - self.abCalInst.e_op))
    #     epick = e_range[targ_i]

    #     jdospick: np.ndarray = jdos[targ_i]
    #     vmin = np.min(jdospick)
    #     vmax = np.max(jdospick)

    #     if (not jdos_dir.exist_fig()) or update_elejdos:
    #         fig, ax = plt.subplots(figsize=(7, 7))
    #         for elei in range(jdospick.shape[-1]):
    #             vi = elei % self.abCalInst.bds_num + 1
    #             ci = elei // self.abCalInst.bds_num + 1

    #             elefname = self.abFileInst.elefname.format(vi, ci)

    #             title = (
    #                 r"$v_{} \to c_{}$".format(vi, ci)
    #                 + "\n"
    #                 + r"$E_{op}$=%.2f meV" % epick
    #             )
    #             PubMethod.cmap_scatters(
    #                 k_arrs[:, 0],
    #                 k_arrs[:, 1],
    #                 jdospick[:, elei],
    #                 bound_vecs=bound_vecs,
    #                 saveInst=jdos_dir,
    #                 fname=elefname,
    #                 vmin=vmin,
    #                 vmax=vmax,
    #                 title=title,
    #                 figax_in=(fig, ax),
    #                 clabel_name="JDOS",
    #             )
    #         plt.close(fig)

    #     return jdos

    # def ediff_plot(self, update_eles=False, levels=20, colors=None):
    #     (
    #         raman_dist,
    #         Mop2,
    #         ediff,
    #         k_arrs,
    #         bound_vecs,
    #         eleplots,
    #     ) = self.abFileInst.abload()

    #     rdist_reallim, rdist_imaglim = PubMethod.sym_limit(
    #         raman_dist, split_realimag=True
    #     )

    #     elet_dir = self.abFileInst.elet_fdir

    #     eleplots = self.abFileInst.elet_ediff_exists()

    #     if eleplots or update_eles:
    #         for ele_col in range(raman_dist.shape[-1]):
    #             vi = ele_col % self.abCalInst.bds_num + 1
    #             ci = ele_col // self.abCalInst.bds_num + 1

    #             elef1name = self.abFileInst.elefname.format(vi, ci) + "_real"
    #             elef2name = self.abFileInst.elefname.format(vi, ci) + "_imag"

    #             title = r"$\theta = {:.2f}\degree$ $v_{} \to c_{}$".format(
    #                 self.abCalInst.haInst.moInst.twist_angle, vi, ci
    #             )

    #             fig, ax_2d = plt.subplots(figsize=(7, 7))
    #             im_var = ax_2d.scatter(
    #                 k_arrs[:, 0],
    #                 k_arrs[:, 1],
    #                 c=np.real(raman_dist[:, ele_col]),
    #                 s=5.5,
    #                 vmin=-rdist_reallim,
    #                 vmax=rdist_reallim,
    #                 marker="h",
    #                 cmap="bwr",
    #             )
    #             ax_2d.plot(bound_vecs[:, 0], bound_vecs[:, 1], "k-")
    #             ax_2d.tricontour(
    #                 k_arrs[:, 0],
    #                 k_arrs[:, 1],
    #                 ediff[:, ele_col],
    #                 levels=levels,
    #                 colors=colors,
    #                 linestyles="dashed",
    #             )

    #             ax_2d.set_aspect("equal")
    #             ax_2d.axis("off")
    #             ax_2d.set_title(title, fontsize=14)
    #             c_ax = PubMethod.add_right_cax(ax_2d, 0.01, 0.01)
    #             cbar = fig.colorbar(im_var, cax=c_ax)
    #             cbar.set_label(
    #                 label="Real part resonance",
    #                 fontsize=12,
    #                 labelpad=13,
    #             )
    #             elet_dir.save_fig(fig, elef1name, subfolder="elet_ediff")

    #             plt.close(fig)

    #             fig, ax_2d = plt.subplots(figsize=(7, 7))
    #             im_var = ax_2d.scatter(
    #                 k_arrs[:, 0],
    #                 k_arrs[:, 1],
    #                 c=np.imag(raman_dist[:, ele_col]),
    #                 s=5.5,
    #                 vmin=-rdist_imaglim,
    #                 vmax=rdist_imaglim,
    #                 marker="h",
    #                 cmap="bwr",
    #             )
    #             ax_2d.plot(bound_vecs[:, 0], bound_vecs[:, 1], "k-")
    #             ax_2d.tricontour(
    #                 k_arrs[:, 0],
    #                 k_arrs[:, 1],
    #                 ediff[:, ele_col],
    #                 levels=levels,
    #                 colors=colors,
    #                 linestyles="dashed",
    #             )

    #             ax_2d.set_aspect("equal")
    #             ax_2d.axis("off")
    #             ax_2d.set_title(title, fontsize=14)
    #             c_ax = PubMethod.add_right_cax(ax_2d, 0.01, 0.01)
    #             cbar = fig.colorbar(im_var, cax=c_ax)
    #             cbar.set_label(
    #                 label="Imaginary part resonance",
    #                 fontsize=12,
    #                 labelpad=13,
    #             )
    #             elet_dir.save_fig(fig, elef2name, subfolder="elet_ediff")

    #             plt.close(fig)

    #     rdist_real = np.sum(np.real(raman_dist), axis=1)
    #     rdist_imag = np.sum(np.imag(raman_dist), axis=1)
    #     fig, ax_2d = plt.subplots(figsize=(7, 7))
    #     im_var = ax_2d.scatter(
    #         k_arrs[:, 0],
    #         k_arrs[:, 1],
    #         c=rdist_real,
    #         s=5.5,
    #         vmin=-rdist_reallim,
    #         vmax=rdist_reallim,
    #         marker="h",
    #         cmap="bwr",
    #     )
    #     ax_2d.plot(bound_vecs[:, 0], bound_vecs[:, 1], "k-")
    #     for ele_col in [0, self.abCalInst.bds_num + 1]:
    #         print("vi: ", ele_col % self.abCalInst.bds_num + 1)
    #         print("ci: ", ele_col // self.abCalInst.bds_num + 1)
    #         ax_2d.tricontour(
    #             k_arrs[:, 0],
    #             k_arrs[:, 1],
    #             ediff[:, ele_col],
    #             levels=levels,
    #             colors=colors,
    #         )

    #     ax_2d.set_aspect("equal")
    #     ax_2d.axis("off")
    #     ax_2d.set_title(
    #         r"$\theta={}\degree$".format(self.abCalInst.haInst.sigs), fontsize=14
    #     )
    #     c_ax = PubMethod.add_right_cax(ax_2d, 0.01, 0.01)
    #     cbar = fig.colorbar(im_var, cax=c_ax)
    #     cbar.set_label(
    #         label="Real part resonance",
    #         fontsize=12,
    #         labelpad=13,
    #     )
    #     elet_dir.save_fig(fig, "rdist_sum_real", subfolder="elet_ediff")

    #     plt.close(fig)

    #     fig, ax_2d = plt.subplots(figsize=(7, 7))
    #     im_var = ax_2d.scatter(
    #         k_arrs[:, 0],
    #         k_arrs[:, 1],
    #         c=rdist_imag,
    #         s=5.5,
    #         vmin=-rdist_imaglim,
    #         vmax=rdist_imaglim,
    #         marker="h",
    #         cmap="bwr",
    #     )
    #     ax_2d.plot(bound_vecs[:, 0], bound_vecs[:, 1], "k-")
    #     for ele_col in [0, self.abCalInst.bds_num + 1]:
    #         ax_2d.tricontour(
    #             k_arrs[:, 0],
    #             k_arrs[:, 1],
    #             ediff[:, ele_col],
    #             levels=levels,
    #             colors=colors,
    #         )

    #     ax_2d.set_aspect("equal")
    #     ax_2d.axis("off")
    #     ax_2d.set_title(
    #         r"$\theta={}\degree$".format(self.abCalInst.haInst.sigs), fontsize=14
    #     )
    #     c_ax = PubMethod.add_right_cax(ax_2d, 0.01, 0.01)
    #     cbar = fig.colorbar(im_var, cax=c_ax)
    #     cbar.set_label(
    #         label="Imaginary part resonance",
    #         fontsize=12,
    #         labelpad=13,
    #     )
    #     elet_dir.save_fig(fig, "rdist_sum_imag", subfolder="elet_ediff")

    #     plt.close(fig)
    #     return raman_dist


class AbsorptionFiles:
    allinfo_fname = "alltrans"
    elefname = "e_{}"

    def __init__(self, abCalInst: AbsorptionCal, ffolder="") -> None:
        self.abCalInst = abCalInst
        self.ffolder = os.path.join(*ffolder.split("/"))

        self._suppinfo = "../{}/{}_{}_{}".format(
            ffolder,
            self.abCalInst.haInst.__class__.__name__,
            self.abCalInst.haInst.sigs,
            self.abCalInst.density,
        )

        self._Mop_fdir = FilesSave("Absorption/Mop2") + self._suppinfo
        self._elet_fdir = FilesSave("Absorption/elet") + self._suppinfo
        self._ediff_fdir = FilesSave("Absorption/ediff") + self._suppinfo
        pass

    def abdir(self):
        return self.elet_fdir

    def abload(self, update_npy=False):
        eleexists = (
            # self.Mop_fdir.exist_fig()
            self.elet_fdir.exist_fig()
            # and self.ediff_fdir.exist_fig()
        )

        if self.existed()[0] and (not update_npy):
            print("Loading: ", self.elet_fdir.target_dir + self.allinfo_fname)
            ab_dist, k_arrs, bound_vecs = (
                self.elet_fdir.load_npy(self.allinfo_fname),
                self.elet_fdir.load_npy("karrs"),
                self.elet_fdir.load_npy("bvecs"),
            )
        else:
            if update_npy:
                print("Updating the npy file...")
            else:
                print(
                    "Cannot find existing files in: ",
                    self.elet_fdir.target_dir,
                    ". Starting new calculations",
                )
            ab_dist, k_arrs, bound_vecs = self.abCalInst.calculate()
            self.elet_fdir.save_npy(self.allinfo_fname, ab_dist)
            self.elet_fdir.save_npy("karrs", k_arrs)
            self.elet_fdir.save_npy("bvecs", bound_vecs)

        return ab_dist, k_arrs, bound_vecs, (not eleexists)

    # def elet_ediff_exists(self):
    #     exists = self.elet_fdir.exist_fig(subfolder="elet_ediff")
    #     return not exists

    # @property
    # def Mop_fdir(self):
    #     return self._Mop_fdir

    @property
    def elet_fdir(self):
        return self._elet_fdir

    # @property
    # def ediff_fdir(self):
    #     return self._ediff_fdir

    @property
    def jdos_dir(self):
        return FilesSave("Absorption/jdos") + self._suppinfo

    def existed(self) -> tuple[bool, bool]:
        """
        # return
        infoexist, figfull
        """
        infoexist = False
        figfull = False
        if (
            # self.Mop_fdir.exist_npy(self.allinfo_fname)
            self.elet_fdir.exist_npy(self.allinfo_fname)
            # and self.ediff_fdir.exist_npy(self.allinfo_fname)
        ):
            infoexist = True
        if os.path.exists(self.elet_fdir.fig_dir) and (
            len(os.listdir(self.elet_fdir.fig_dir)) == self.abCalInst.bds_num**2
        ):
            figfull = True

        return infoexist, figfull


def main():
    fileInstnames = ["hello", "yes", "get"]
    return


if __name__ == "__main__":
    main()
