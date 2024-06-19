from ..abc.abmoire import ABContiMoHa
from ..abc.abcal import ABCal
from ..pubmeth.pubmeth import DefinedFuncs

from ..multical.multicorecal import MultiCal
import sys

import numpy as np


class JdosCal(ABCal):
    def __init__(
        self,
        haInst: ABContiMoHa,
        density: int = 70,
        cal_corenum: int = 3,
        e_range=np.linspace(100, 2500, 200),
        broadening=1,
        vc_num=None,
        cal_hint=False,
        large_scale_cal=False,
    ) -> None:
        super().__init__(haInst, density, cal_corenum)

        self.e_range = e_range
        self.broadening = broadening

        self.vc_num = vc_num
        self.cal_hint = cal_hint
        self.large_scal_cal = large_scale_cal

    def energies_cal(self, k_arr):
        h = self.haInst.h(k_arr)

        eig_vals = np.real(np.linalg.eig(h)[0])

        mid_i = len(eig_vals) // 2

        eig_vals.sort()

        v_slice = (
            slice(mid_i - 1, -(len(eig_vals) + 1), -1)
            if self.vc_num is None
            else slice(mid_i - 1, mid_i - 1 - self.vc_num, -1)
        )
        c_slice = (
            slice(mid_i, len(eig_vals))
            if self.vc_num is None
            else slice(mid_i, mid_i + self.vc_num)
        )

        v_e: np.ndarray = eig_vals[v_slice]
        c_e: np.ndarray = eig_vals[c_slice]

        vee = np.kron(np.ones((1, len(v_e))), v_e.reshape((-1, 1)))
        cee = np.kron(np.ones((len(c_e), 1)), c_e.reshape((1, -1)))

        je: np.ndarray = cee - vee
        ### The first row
        #   c1-v1, c1-v2, c1-v3, ..., c1-vn

        return je

    def calculate(self):
        k_arrs, bound_vs = self.kps_in_BZ()

        je = MultiCal(
            self.energies_cal,
            k_arrs,
            [],
            core=self.calcoren,
            disable_hint=(not self.cal_hint),
        ).calculate()
        je = np.array(je)

        print("Shape of the joint energy matrix: ", je.shape)
        print("Size of joint energy (MB): ", sys.getsizeof(je) / 1024**2)
        np.save("tmp_jdos.npy", je)

        if not self.large_scal_cal:
            jdos = DefinedFuncs.deltaF_arct(je, self.e_range, a=self.broadening)
        else:
            print("Large scale calculations...")
            jdos = []
            for ele_e in self.e_range:
                ele_jdos = DefinedFuncs.deltaF_arct(je, ele_e, a=self.broadening)
                ele_jdos = np.sum(ele_jdos)
                jdos.append(ele_jdos)
            jdos = np.array(jdos)

        print("Shape of the joint energy matrix: ", jdos.shape)
        print("Size of joint energy (MB): ", sys.getsizeof(jdos) / 1024**2)

        return je, jdos  # , k_arrs, bound_vs


def main():
    return


if __name__ == "__main__":
    main()
