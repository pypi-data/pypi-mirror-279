from ..abc.abmoire import ABCommGraMoire
import numpy as np
import matplotlib.pyplot as plt
from ..filesop.filesave import FilesSave


class StruPlot:
    def __init__(self, moInst: ABCommGraMoire) -> None:
        self.moInst = moInst

        self.space = self.moInst.a0 / np.sqrt(3)
        self.filrInst = FilesSave("Structures")

    def plot(self):
        vecs = self.moInst.equal_rvecs()
        layers_list = [
            vecs[
                len(vecs)
                // len(self.moInst.lindexes)
                * i : len(vecs)
                // len(self.moInst.lindexes)
                * (i + 1),
                :,
            ]
            for i in range(len(self.moInst.lindexes))
        ]

        bound_vecs = np.vstack(
            [
                np.zeros((2, 2)),
                self.moInst.R1,
                self.moInst.R1 + self.moInst.R2,
                self.moInst.R2,
                np.zeros((2, 2)),
            ]
        )

        fname = self.moInst.__class__.__name__ + "_{:.2f}".format(
            self.moInst.twist_angle
        )
        fig, ax_stru = plt.subplots()

        for ele_vecs in layers_list:
            ele_lel = np.kron(np.ones((len(ele_vecs), 1)), ele_vecs)
            ele_ler = np.kron(ele_vecs, np.ones((len(ele_vecs), 1)))
            diff_arrs = ele_lel - ele_ler
            diff_norms = np.linalg.norm(diff_arrs, axis=1)
            diff_norms: np.ndarray = diff_norms.reshape((len(ele_vecs), len(ele_vecs)))
            nearest_boolmat = np.abs(diff_norms - self.space) < 0.01

            plt.close()
            for ele_i in range(len(nearest_boolmat)):
                (out_bool_i,) = np.where(nearest_boolmat[ele_i] == True)
                out_i = np.vstack(
                    [ele_i * np.ones((1, len(out_bool_i))), out_bool_i]
                ).T.reshape((-1,))
                out_i = np.int0(out_i)

                out_vecs = ele_vecs[out_i]
                ax_stru.plot(out_vecs[:, 0], out_vecs[:, 1], "k")
        ax_stru.plot(bound_vecs[:, 0], bound_vecs[:, 1], "r")
        ax_stru.set_aspect("equal")
        ax_stru.set_xlabel("x ($\AA$)", fontsize=12)
        ax_stru.set_ylabel("y ($\AA$)", fontsize=12)
        ax_stru.set_title(
            r"$\theta={:.2f}\degree$".format(self.moInst.twist_angle), fontsize=14
        )
        ax_stru.set_xlim(ax_stru.get_xlim())
        ax_stru.set_ylim(ax_stru.get_ylim())
        self.filrInst.save_fig(fig, fname)
