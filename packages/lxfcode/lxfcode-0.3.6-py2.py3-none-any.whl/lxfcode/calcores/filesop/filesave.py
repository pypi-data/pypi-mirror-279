import os
import numpy as np
from matplotlib.figure import Figure
import cv2


class FilesSave:
    root_dir = os.getcwd()

    def __init__(self, dirname: str = "Data") -> None:
        self.dir_levels = dirname.split("/")

        self.target_dir = os.path.join(self.root_dir, *self.dir_levels) + os.sep
        self.npy_dir = self.target_dir + "npy" + os.sep
        self.fig_dir = self.target_dir + "fig" + os.sep

        # if not os.path.exists(self.target_dir):
        #     os.makedirs(self.target_dir)
        # if not os.path.exists(self.fig_dir):
        #     os.makedirs(self.fig_dir)

    def __add__(self, sublevels: str):
        levels = sublevels.split("/")
        if levels[0] == "..":
            levels.pop(0)
            new_level = self.dir_levels.copy()
            new_level.insert(1, levels[0])
            levels.pop(0)

            sumdir = os.path.join(*new_level, *levels)
            return FilesSave(sumdir)
        sumdir = os.path.join(*self.dir_levels, *levels)
        return FilesSave(sumdir)

    def __radd__(self, sublevels: str):
        return self.__add__(sublevels)

    def save_npy(self, fname, npy):
        if not os.path.exists(self.npy_dir):
            os.makedirs(self.npy_dir)
        np.save(self.npy_dir + fname + ".npy", npy)

    def exist_npy(self, fname):
        if os.path.exists(self.npy_dir + fname + ".npy"):
            return True

    def load_npy(self, fname):
        if self.exist_npy(fname):
            return np.load(self.npy_dir + fname + ".npy")
        else:
            raise FileNotFoundError("No npy file named: ", fname)

    def load_fig_path(self, fname, subfolder="") -> str:
        folder_levels = subfolder.split("/")
        figdir = os.path.join(self.fig_dir, *folder_levels) + os.sep
        if (
            bool(subfolder)
            and os.path.exists(figdir)
            and os.path.exists(figdir + fname)
        ):
            return figdir + fname
        else:
            raise FileNotFoundError(
                "input subfolder doesn't exist or file doesn't exist"
            )

    def save_fig(self, fig: Figure, fname, save_pdf=False, subfolder=""):
        if not os.path.exists(self.fig_dir):
            os.makedirs(self.fig_dir)
        folder_levels = subfolder.split("/")
        figdir = os.path.join(self.fig_dir, *folder_levels) + os.sep
        if not os.path.exists(figdir):
            os.makedirs(figdir)

        fig.savefig(
            figdir + fname + ".png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        if save_pdf:
            fig.savefig(
                figdir + fname + ".pdf",
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )

    def exist_fig(self, fname="", subfolder=""):
        folder_levels = subfolder.split("/")
        figdir = os.path.join(self.fig_dir, *folder_levels) + os.sep
        if bool(fname):
            if os.path.exists(figdir + fname + ".png"):
                return True
            return False
        if os.path.exists(figdir) and os.listdir(figdir):
            return True
        return False

    def save_movie(
        self, figs_list: list[str], mv_fname: str, frames=25, subfolder="", fig_dir=None
    ):
        if fig_dir is None:
            figs_list = [self.fig_dir + ele_fname + ".png" for ele_fname in figs_list]
        folder_levels = subfolder.split("/")
        folder_levels.insert(0, "mv")
        mv_dir = os.path.join(self.target_dir, *folder_levels) + os.sep

        if not os.path.exists(mv_dir):
            os.makedirs(mv_dir)
        img_example = cv2.imread(figs_list[0])
        img_shape = img_example.shape[:2]
        print("shape: ", img_shape)

        writer = cv2.VideoWriter(
            mv_dir + mv_fname + ".mp4",
            cv2.VideoWriter_fourcc("m", "p", "4", "v"),
            frames,
            img_shape[::-1],
            True,
        )
        shapes_list = []
        for elef in figs_list:
            read_img = cv2.imread(elef)
            read_img = cv2.resize(read_img, dsize=img_shape[::-1])
            writer.write(read_img)
            shapes_list.append(read_img.shape[:2])
        writer.release()


# class EleFileSave:
#     allinfo_fname = "alltrans"
#     elefname = "v{}_c{}"

#     def __init__(
#         self,
#         haInst: ABMoHa,
#         ffolder="",
#         suppinfo_plus: list[Union[str, float]] = None,
#         dirnames: list[str] = None,
#     ) -> None:
#         self.haInst = haInst
#         self.ffolder = os.path.join(*ffolder.split("/"))

#         self._suppinfo = "../{}/{}_{}".format(
#             ffolder,
#             self.haInst.__class__.__name__,
#             self.haInst.sigs,
#         )
#         supp_plus = [str(ele) for ele in suppinfo_plus]

#         self._suppinfo: str = "_".join(self._suppinfo, supp_plus)

#         self._Mop_fdir = FilesSave("Raman/Mop2") + self._suppinfo
#         self._elet_fdir = FilesSave("Raman/elet") + self._suppinfo
#         self._ediff_fdir = FilesSave("Raman/ediff") + self._suppinfo
#         pass

#     def ramandir(self):
#         return self.Mop_fdir, self.elet_fdir, self.ediff_fdir

#     def ramanload(self):
#         eleexists = (
#             self.Mop_fdir.exist_fig()
#             and self.elet_fdir.exist_fig()
#             and self.ediff_fdir.exist_fig()
#         )

#         if self.existed()[0]:
#             print("Loading: ", self.elet_fdir.target_dir + self.allinfo_fname)
#             raman_dist, Mop2, ediff, k_arrs, bound_vecs = (
#                 self.elet_fdir.load_npy(self.allinfo_fname),
#                 self.Mop_fdir.load_npy(self.allinfo_fname),
#                 self.ediff_fdir.load_npy(self.allinfo_fname),
#                 self.ediff_fdir.load_npy("karrs"),
#                 self.ediff_fdir.load_npy("bvecs"),
#             )
#         else:
#             print(
#                 "Cannot find existing files in: ",
#                 self.Mop_fdir.target_dir,
#                 ". Starting new calculations",
#             )
#             raman_dist, Mop2, ediff, k_arrs, bound_vecs = self.rCalInst.calculate()
#             self.elet_fdir.save_npy(self.allinfo_fname, raman_dist)
#             self.Mop_fdir.save_npy(self.allinfo_fname, Mop2)
#             self.ediff_fdir.save_npy(self.allinfo_fname, ediff)
#             self.ediff_fdir.save_npy("karrs", k_arrs)
#             self.ediff_fdir.save_npy("bvecs", bound_vecs)

#         return raman_dist, Mop2, ediff, k_arrs, bound_vecs, (not eleexists)

#     def elet_ediff_exists(self):
#         exists = self.elet_fdir.exist_fig(subfolder="elet_ediff")
#         return not exists

#     @property
#     def Mop_fdir(self):
#         return self._Mop_fdir

#     @property
#     def elet_fdir(self):
#         return self._elet_fdir

#     @property
#     def ediff_fdir(self):
#         return self._ediff_fdir

#     @property
#     def jdos_dir(self):
#         return FilesSave("Raman/jdos") + self._suppinfo

#     def existed(self) -> tuple[bool, bool]:
#         """
#         # return
#         infoexist, figfull
#         """
#         infoexist = False
#         figfull = False
#         if (
#             self.Mop_fdir.exist_npy(self.allinfo_fname)
#             and self.elet_fdir.exist_npy(self.allinfo_fname)
#             and self.ediff_fdir.exist_npy(self.allinfo_fname)
#         ):
#             infoexist = True
#         if len(os.listdir(self.Mop_fdir.fig_dir)) == self.rCalInst.bds_num**2:
#             figfull = True

#         return infoexist, figfull


def main():
    f1 = FilesSave("Raman/hello") + "../good"
    print(f1.target_dir)
    return


if __name__ == "__main__":
    main()
