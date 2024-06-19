from ..jdos.jdos_cal import JdosCal, DefinedFuncs
from ..filesop.filesave import FilesSave
import matplotlib.pyplot as plt
import numpy as np


class JdosPlot:
    def __init__(self, jdosCal: JdosCal, ffolder="", update_npy=False) -> None:
        self.jCalInst = jdosCal

        self._supp_info = "../{}/{}_{}_{}".format(
            ffolder,
            self.jCalInst.haInst.__class__.__name__,
            self.jCalInst.haInst.sigs,
            self.jCalInst.density,
        )

        self.jFolderInst = FilesSave("JDOS/jdos") + self._supp_info
        self.jdos_info = "jdos_{}".format(self.jCalInst.broadening)
        self.je_info = "je"

        self.update_npy = update_npy

    def _load(self):
        if self.jFolderInst.exist_npy(self.jdos_info) and (not self.update_npy):
            print("Loading existing npy file...")
            jdos = self.jFolderInst.load_npy(self.jdos_info)
        else:
            print("Calculating...")
            if self.jFolderInst.exist_npy(self.je_info):
                print("Using the existing npy file...")
                je = self.jFolderInst.load_npy(self.je_info)
                if not self.jCalInst.large_scal_cal:
                    jdos = DefinedFuncs.deltaF_arct(
                        je, self.jCalInst.e_range, a=self.jCalInst.broadening
                    )
                else:
                    print("Large scale calculations...")
                    jdos = []
                    for ele_e in self.jCalInst.e_range:
                        ele_jdos = DefinedFuncs.deltaF_arct(
                            je, ele_e, a=self.jCalInst.broadening
                        )
                        ele_jdos = np.sum(ele_jdos)
                        jdos.append(ele_jdos)
                    jdos = np.array(jdos)
            else:
                print("calculating...")
                je, jdos = self.jCalInst.calculate()
            self.jFolderInst.save_npy(self.jdos_info, jdos)
            self.jFolderInst.save_npy(self.je_info, je)
        return jdos

    def plot(self):
        jdos = self._load()
        if not self.jCalInst.large_scal_cal:
            jdos: np.ndarray = jdos.sum(axis=-1).sum(axis=-1).sum(axis=-1)
        else:
            print("The array is already reduced to one dimension: ", jdos.shape)
            pass
        fig, ax_jdos = plt.subplots()
        ax_jdos.plot(self.jCalInst.e_range, jdos)
        ax_jdos.set_aspect("auto")
        ax_jdos.set_xlabel("E (meV)", fontsize=12)
        ax_jdos.set_ylabel("JDOS", fontsize=12)
        ax_jdos.set_title("", fontsize=14)
        ax_jdos.set_xlim(ax_jdos.get_xlim())
        ax_jdos.set_ylim(ax_jdos.get_ylim())
        self.jFolderInst.save_fig(fig, fname="jdos_{}".format(self.jCalInst.broadening))

        return


class JdosFiles:
    def __init__(self) -> None:
        pass
