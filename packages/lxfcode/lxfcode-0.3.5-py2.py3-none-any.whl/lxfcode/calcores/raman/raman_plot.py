from ..raman.raman_cal import RamanCal
import numpy as np
from ..filesop.filesave import FilesSave
import matplotlib.pyplot as plt
from ..pubmeth.pubmeth import PubMethod, DefinedFuncs
import os
from typing import Literal


plt.rc("font", family="Times New Roman")  # change the font of plot
plt.rcParams["mathtext.fontset"] = "stix"


class RamanPlot:
    fontsize = 12
    titlesize = 14

    def __init__(self, rCalInst: RamanCal, ffolder="", disable_elet=False) -> None:
        self.rCalInst = rCalInst
        self.rFileInst = RamanFiles(self.rCalInst, ffolder)

        self.disable_elet = disable_elet
        pass

    def _plot_ele_raman(
        self,
        raman_dist: np.ndarray,
        Mop2,
        ediff,
        k_arrs,
        bound_vecs,
        Mop_dir,
        elet_dir,
        ediff_dir,
    ):
        rdist_reallim, rdist_imaglim = PubMethod.sym_limit(
            raman_dist, split_realimag=True
        )
        mop2_lim = PubMethod.sym_limit(Mop2)
        fig, ax = plt.subplots(figsize=(7, 7))
        for ele_col in range(raman_dist.shape[-1]):
            vi = ele_col % self.rCalInst.bds_num + 1
            ci = ele_col // self.rCalInst.bds_num + 1

            fname = self.rFileInst.elefname.format(vi, ci)
            title = r"$\theta = {:.2f}\degree$ $v_{} \to c_{}$".format(
                self.rCalInst.haInst.moInst.twist_angle, vi, ci
            )

            PubMethod.cmap_scatters(
                k_arrs[:, 0],
                k_arrs[:, 1],
                np.real(raman_dist[:, ele_col]),
                bound_vecs,
                elet_dir,
                fname + "_real",
                title=title,
                vmin=-rdist_reallim,
                vmax=rdist_reallim,
                clabel_name="Resonance intensity (a.u.)",
                figax_in=(fig, ax),
            )
            PubMethod.cmap_scatters(
                k_arrs[:, 0],
                k_arrs[:, 1],
                np.imag(raman_dist[:, ele_col]),
                bound_vecs,
                elet_dir,
                fname + "_imag",
                title=title,
                vmin=-rdist_imaglim,
                vmax=rdist_imaglim,
                clabel_name="Resonance intensity (a.u.)",
                figax_in=(fig, ax),
            )
            PubMethod.cmap_scatters(
                k_arrs[:, 0],
                k_arrs[:, 1],
                Mop2[:, ele_col],
                bound_vecs,
                Mop_dir,
                fname,
                title=title,
                vmin=-mop2_lim,
                vmax=mop2_lim,
                figax_in=(fig, ax),
            )
            PubMethod.cmap_scatters(
                k_arrs[:, 0],
                k_arrs[:, 1],
                ediff[:, ele_col],
                bound_vecs,
                ediff_dir,
                fname,
                title=title,
                clabel_name=r"$\Delta E$",
                cmap="jet",
                figax_in=(fig, ax),
            )
        plt.close(fig)

    def plot(self, update_elet=False):
        Mop_dir, elet_dir, ediff_dir = self.rFileInst.ramandir()
        (
            raman_dist,
            Mop2,
            ediff,
            k_arrs,
            bound_vecs,
            eleplots,
        ) = self.rFileInst.ramanload()

        rdist_reallim, rdist_imaglim = PubMethod.sym_limit(
            raman_dist, split_realimag=True
        )

        if (not self.disable_elet) and (eleplots or update_elet):
            print("Plotting element transitions...")
            self._plot_ele_raman(
                raman_dist,
                Mop2,
                ediff,
                k_arrs,
                bound_vecs,
                Mop_dir,
                elet_dir,
                ediff_dir,
            )

        rdist_real = np.sum(np.real(raman_dist), axis=1)
        rdist_imag = np.sum(np.imag(raman_dist), axis=1)
        PubMethod.cmap_scatters(
            k_arrs[:, 0],
            k_arrs[:, 1],
            rdist_real,
            bound_vecs,
            elet_dir,
            "rdist_sum_real",
            title=r"$\theta={}\degree$".format(self.rCalInst.haInst.sigs),
            vmin=-rdist_reallim,
            vmax=rdist_reallim,
            clabel_name="Resonance intensity (a.u.)",
        )
        PubMethod.cmap_scatters(
            k_arrs[:, 0],
            k_arrs[:, 1],
            rdist_imag,
            bound_vecs,
            elet_dir,
            "rdist_sum_imag",
            title=r"$\theta={}\degree$".format(self.rCalInst.haInst.sigs),
            vmin=-rdist_imaglim,
            vmax=rdist_imaglim,
            clabel_name="Resonance intensity (a.u.)",
        )
        return raman_dist

    def jdos_plot(
        self,
        e_range=np.linspace(100, 2500, 200),
        broadening=1,
        update_elejdos=False,
        update_npy=False,
        plot_type: Literal["jdos", "jdosmop"] = "jdos",
    ):
        jdos_dir = self.rFileInst.jdos_dir

        (
            raman_dist,
            Mop2,
            ediff,
            k_arrs,
            bound_vecs,
            eleplots,
        ) = self.rFileInst.ramanload()

        fname = "{}_{:.2f}".format(plot_type, broadening)
        if jdos_dir.exist_npy(fname) and (not update_npy):
            jdos = np.real(jdos_dir.load_npy(fname))
        else:
            jdos = DefinedFuncs.deltaF_arct(ediff, e_range, a=broadening)
            if plot_type == "jdos":
                jdos_dir.save_npy(fname, jdos)
            elif plot_type == "jdosmop":
                Mop_e: np.ndarray = np.kron(np.ones((jdos.shape[0], 1, 1)), Mop2)
                jdos = np.real(jdos * Mop_e)
                jdos_dir.save_npy(fname, np.real(jdos))
                print("Complete saving: ", fname)
        targ_i = np.argmin(abs(e_range - self.rCalInst.e_op))
        epick = e_range[targ_i]

        jdospick: np.ndarray = jdos[targ_i]
        vmin = np.min(jdospick)
        vmax = np.max(jdospick)

        if (not jdos_dir.exist_fig()) or update_elejdos:
            fig, ax = plt.subplots(figsize=(7, 7))
            for elei in range(jdospick.shape[-1]):
                vi = elei % self.rCalInst.bds_num + 1
                ci = elei // self.rCalInst.bds_num + 1

                elefname = self.rFileInst.elefname.format(vi, ci)

                title = (
                    r"$v_{} \to c_{}$".format(vi, ci)
                    + "\n"
                    + r"$E_{op}$=%.2f meV" % epick
                )
                PubMethod.cmap_scatters(
                    k_arrs[:, 0],
                    k_arrs[:, 1],
                    jdospick[:, elei],
                    bound_vecs=bound_vecs,
                    saveInst=jdos_dir,
                    fname=elefname,
                    vmin=vmin,
                    vmax=vmax,
                    title=title,
                    figax_in=(fig, ax),
                    clabel_name="JDOS",
                )
            plt.close(fig)

        return jdos

    def ediff_plot(self, update_eles=False, levels=20, colors=None):
        (
            raman_dist,
            Mop2,
            ediff,
            k_arrs,
            bound_vecs,
            eleplots,
        ) = self.rFileInst.ramanload()

        rdist_reallim, rdist_imaglim = PubMethod.sym_limit(
            raman_dist, split_realimag=True
        )

        elet_dir = self.rFileInst.elet_fdir

        eleplots = self.rFileInst.elet_ediff_exists()

        if eleplots or update_eles:
            for ele_col in range(raman_dist.shape[-1]):
                vi = ele_col % self.rCalInst.bds_num + 1
                ci = ele_col // self.rCalInst.bds_num + 1

                elef1name = self.rFileInst.elefname.format(vi, ci) + "_real"
                elef2name = self.rFileInst.elefname.format(vi, ci) + "_imag"

                title = r"$\theta = {:.2f}\degree$ $v_{} \to c_{}$".format(
                    self.rCalInst.haInst.moInst.twist_angle, vi, ci
                )

                fig, ax_2d = plt.subplots(figsize=(7, 7))
                im_var = ax_2d.scatter(
                    k_arrs[:, 0],
                    k_arrs[:, 1],
                    c=np.real(raman_dist[:, ele_col]),
                    s=5.5,
                    vmin=-rdist_reallim,
                    vmax=rdist_reallim,
                    marker="h",
                    cmap="bwr",
                )
                ax_2d.plot(bound_vecs[:, 0], bound_vecs[:, 1], "k-")
                ax_2d.tricontour(
                    k_arrs[:, 0],
                    k_arrs[:, 1],
                    ediff[:, ele_col],
                    levels=levels,
                    colors=colors,
                    linestyles="dashed",
                )

                ax_2d.set_aspect("equal")
                ax_2d.axis("off")
                ax_2d.set_title(title, fontsize=14)
                c_ax = PubMethod.add_right_cax(ax_2d, 0.01, 0.01)
                cbar = fig.colorbar(im_var, cax=c_ax)
                cbar.set_label(
                    label="Real part resonance",
                    fontsize=12,
                    labelpad=13,
                )
                elet_dir.save_fig(fig, elef1name, subfolder="elet_ediff")

                plt.close(fig)

                fig, ax_2d = plt.subplots(figsize=(7, 7))
                im_var = ax_2d.scatter(
                    k_arrs[:, 0],
                    k_arrs[:, 1],
                    c=np.imag(raman_dist[:, ele_col]),
                    s=5.5,
                    vmin=-rdist_imaglim,
                    vmax=rdist_imaglim,
                    marker="h",
                    cmap="bwr",
                )
                ax_2d.plot(bound_vecs[:, 0], bound_vecs[:, 1], "k-")
                ax_2d.tricontour(
                    k_arrs[:, 0],
                    k_arrs[:, 1],
                    ediff[:, ele_col],
                    levels=levels,
                    colors=colors,
                    linestyles="dashed",
                )

                ax_2d.set_aspect("equal")
                ax_2d.axis("off")
                ax_2d.set_title(title, fontsize=14)
                c_ax = PubMethod.add_right_cax(ax_2d, 0.01, 0.01)
                cbar = fig.colorbar(im_var, cax=c_ax)
                cbar.set_label(
                    label="Imaginary part resonance",
                    fontsize=12,
                    labelpad=13,
                )
                elet_dir.save_fig(fig, elef2name, subfolder="elet_ediff")

                plt.close(fig)

        rdist_real = np.sum(np.real(raman_dist), axis=1)
        rdist_imag = np.sum(np.imag(raman_dist), axis=1)
        fig, ax_2d = plt.subplots(figsize=(7, 7))
        im_var = ax_2d.scatter(
            k_arrs[:, 0],
            k_arrs[:, 1],
            c=rdist_real,
            s=5.5,
            vmin=-rdist_reallim,
            vmax=rdist_reallim,
            marker="h",
            cmap="bwr",
        )
        ax_2d.plot(bound_vecs[:, 0], bound_vecs[:, 1], "k-")
        for ele_col in [0, self.rCalInst.bds_num + 1]:
            print("vi: ", ele_col % self.rCalInst.bds_num + 1)
            print("ci: ", ele_col // self.rCalInst.bds_num + 1)
            ax_2d.tricontour(
                k_arrs[:, 0],
                k_arrs[:, 1],
                ediff[:, ele_col],
                levels=levels,
                colors=colors,
            )

        ax_2d.set_aspect("equal")
        ax_2d.axis("off")
        ax_2d.set_title(
            r"$\theta={}\degree$".format(self.rCalInst.haInst.sigs), fontsize=14
        )
        c_ax = PubMethod.add_right_cax(ax_2d, 0.01, 0.01)
        cbar = fig.colorbar(im_var, cax=c_ax)
        cbar.set_label(
            label="Real part resonance",
            fontsize=12,
            labelpad=13,
        )
        elet_dir.save_fig(fig, "rdist_sum_real", subfolder="elet_ediff")

        plt.close(fig)

        fig, ax_2d = plt.subplots(figsize=(7, 7))
        im_var = ax_2d.scatter(
            k_arrs[:, 0],
            k_arrs[:, 1],
            c=rdist_imag,
            s=5.5,
            vmin=-rdist_imaglim,
            vmax=rdist_imaglim,
            marker="h",
            cmap="bwr",
        )
        ax_2d.plot(bound_vecs[:, 0], bound_vecs[:, 1], "k-")
        for ele_col in [0, self.rCalInst.bds_num + 1]:
            ax_2d.tricontour(
                k_arrs[:, 0],
                k_arrs[:, 1],
                ediff[:, ele_col],
                levels=levels,
                colors=colors,
            )

        ax_2d.set_aspect("equal")
        ax_2d.axis("off")
        ax_2d.set_title(
            r"$\theta={}\degree$".format(self.rCalInst.haInst.sigs), fontsize=14
        )
        c_ax = PubMethod.add_right_cax(ax_2d, 0.01, 0.01)
        cbar = fig.colorbar(im_var, cax=c_ax)
        cbar.set_label(
            label="Imaginary part resonance",
            fontsize=12,
            labelpad=13,
        )
        elet_dir.save_fig(fig, "rdist_sum_imag", subfolder="elet_ediff")

        plt.close(fig)
        return raman_dist

    def raman_eop_plot(self, e_range: np.ndarray = np.linspace(10, 3000, 200)):
        (
            raman_dist,
            Mop2,
            ediff,
            k_arrs,
            bound_vecs,
            eleplots,
        ) = self.rFileInst.ramanload()

        dims = [1] * len(Mop2.shape)

        e_e = np.kron(e_range.reshape((len(e_range), *dims)), np.ones(Mop2.shape))

        Mop2_e: np.ndarray = np.kron(np.ones((len(e_range), *dims)), Mop2)
        ediff_e: np.ndarray = np.kron(np.ones((len(e_range), *dims)), ediff)

        raman_eles_e: np.ndarray = Mop2_e / (
            (e_e - ediff_e - 1j * self.rCalInst.gamma)
            * (e_e - ediff_e - self.rCalInst.e_ph - 1j * self.rCalInst.gamma)
        )

        return raman_eles_e, e_range


class RamanFiles:
    allinfo_fname = "alltrans"
    elefname = "v{}_c{}"

    def __init__(self, rCalInst: RamanCal, ffolder="") -> None:
        self.rCalInst = rCalInst
        self.ffolder = os.path.join(*ffolder.split("/"))

        self._suppinfo = "../{}/{}_{}_{}".format(
            ffolder,
            self.rCalInst.haInst.__class__.__name__,
            self.rCalInst.haInst.sigs,
            self.rCalInst.density,
        )

        self._Mop_fdir = FilesSave("Raman/Mop2") + self._suppinfo
        self._elet_fdir = FilesSave("Raman/elet") + self._suppinfo
        self._ediff_fdir = FilesSave("Raman/ediff") + self._suppinfo
        pass

    def ramandir(self):
        return self.Mop_fdir, self.elet_fdir, self.ediff_fdir

    def ramanload(self):
        eleexists = (
            self.Mop_fdir.exist_fig()
            and self.elet_fdir.exist_fig()
            and self.ediff_fdir.exist_fig()
        )

        if self.existed()[0]:
            print("Loading: ", self.elet_fdir.target_dir + self.allinfo_fname)
            raman_dist, Mop2, ediff, k_arrs, bound_vecs = (
                self.elet_fdir.load_npy(self.allinfo_fname),
                self.Mop_fdir.load_npy(self.allinfo_fname),
                self.ediff_fdir.load_npy(self.allinfo_fname),
                self.ediff_fdir.load_npy("karrs"),
                self.ediff_fdir.load_npy("bvecs"),
            )
        else:
            print(
                "Cannot find existing files in: ",
                self.Mop_fdir.target_dir,
                ". Starting new calculations",
            )
            raman_dist, Mop2, ediff, k_arrs, bound_vecs = self.rCalInst.calculate()
            self.elet_fdir.save_npy(self.allinfo_fname, raman_dist)
            self.Mop_fdir.save_npy(self.allinfo_fname, Mop2)
            self.ediff_fdir.save_npy(self.allinfo_fname, ediff)
            self.ediff_fdir.save_npy("karrs", k_arrs)
            self.ediff_fdir.save_npy("bvecs", bound_vecs)

        return raman_dist, Mop2, ediff, k_arrs, bound_vecs, (not eleexists)

    def elet_ediff_exists(self):
        exists = self.elet_fdir.exist_fig(subfolder="elet_ediff")
        return not exists

    @property
    def Mop_fdir(self):
        return self._Mop_fdir

    @property
    def elet_fdir(self):
        return self._elet_fdir

    @property
    def ediff_fdir(self):
        return self._ediff_fdir

    @property
    def jdos_dir(self):
        return FilesSave("Raman/jdos") + self._suppinfo

    def existed(self) -> tuple[bool, bool]:
        """
        # return
        infoexist, figfull
        """
        infoexist = False
        figfull = False
        if (
            self.Mop_fdir.exist_npy(self.allinfo_fname)
            and self.elet_fdir.exist_npy(self.allinfo_fname)
            and self.ediff_fdir.exist_npy(self.allinfo_fname)
        ):
            infoexist = True
        if os.path.exists(self.Mop_fdir.fig_dir) and (
            len(os.listdir(self.Mop_fdir.fig_dir)) == self.rCalInst.bds_num**2
        ):
            figfull = True

        return infoexist, figfull


def main():
    fileInstnames = ["hello", "yes", "get"]
    return


if __name__ == "__main__":
    main()
