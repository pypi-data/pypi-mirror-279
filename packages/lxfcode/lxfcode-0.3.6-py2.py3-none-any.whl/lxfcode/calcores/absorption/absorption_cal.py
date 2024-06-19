from ..abc.abmoire import ABContiMoHa
import numpy as np
from ..multical.multicorecal import MultiCal
from ..abc.abcal import ABCal
from ..pubmeth.consts import *
import sys


class AbsorptionCal(ABCal):
    def __init__(
        self,
        hInst: ABContiMoHa,
        density: int = 70,
        cal_corenum: int = 3,
        e_range=np.linspace(10, 2500, 400),
        interval_k=0.0001,
        bds_num: int = 5,
        gamma=100,
        e_phonon=196,
        degeneracy_factor=1,
    ) -> None:
        super().__init__(hInst, density, cal_corenum)

        self.e_range = e_range

        self.bds_num = bds_num
        self.ki = interval_k
        self.gamma = gamma
        self.e_ph = e_phonon

        if hasattr(self.haInst.moInst, "areaM"):
            area = self.haInst.moInst.areaM
        else:
            area = self.haInst.moInst.areaO

        self.renorm_const = (
            degeneracy_factor
            * c_eV**2
            / (h_bar_eV * c_speed * epsilon_0_eV)
            / int(self.density**2)
            / area
        )

    def ab_i(self, k_arr):
        hc = self.haInst.h(k_arr)

        hxd = (self.haInst.h(k_arr + np.array([self.ki, 0])) - hc) / (
            self.ki * self.haInst.moInst.renormed_BZ_K_side
        )
        hyd = (self.haInst.h(k_arr + np.array([0, self.ki])) - hc) / (
            self.ki * self.haInst.moInst.renormed_BZ_K_side
        )
        # print("K side: ", self.haInst.moInst.renormed_BZ_K_side)

        eig_vals, eig_vecs = np.linalg.eig(hc)

        mid_i = len(eig_vals) // 2

        v_slice = (
            slice(mid_i - 1, mid_i - 1 - self.bds_num, -1)
            if mid_i - 1 - self.bds_num >= 0
            else slice(mid_i - 1, -(len(eig_vals) + 1), -1)
        )
        c_slice = (
            slice(mid_i, mid_i + self.bds_num)
            if mid_i + self.bds_num <= len(eig_vals)
            else slice(mid_i, len(eig_vals))
        )

        v_energy_arr: np.ndarray = eig_vals[np.argsort(np.real(eig_vals))[v_slice]]
        v_states_arr: np.ndarray = eig_vecs.T[np.argsort(np.real(eig_vals))[v_slice]]

        c_energy_arr: np.ndarray = eig_vals[np.argsort(np.real(eig_vals))[c_slice]]
        c_states_arr: np.ndarray = eig_vecs.T[np.argsort(np.real(eig_vals))[c_slice]]

        bds_num = len(v_energy_arr)

        hx = np.conj(c_states_arr) @ hxd @ v_states_arr.T
        hy = np.conj(c_states_arr) @ hyd @ v_states_arr.T

        Mop2: np.ndarray = abs(hx) ** 2 + abs(hy) ** 2  #   n by n matrix

        ediff: np.ndarray = np.kron(
            c_energy_arr.reshape((-1, 1)), np.ones((1, bds_num))
        ) - np.kron(
            np.ones((bds_num, 1)), v_energy_arr.reshape((1, -1))
        )  #   n by n matrix

        ab_eles_arr = []
        for ele_e in self.e_range:
            tmp_ab = Mop2 * self.gamma / ((ediff - ele_e) ** 2 + self.gamma**2)
            ab_eles_arr.append(np.sum(tmp_ab / ele_e * self.renorm_const))
        ab_eles_arr = np.array(ab_eles_arr)  #   (e_range) array

        # ab_eles_mat = ab_eles_mat.reshape((-1,))  #   (e_range) array
        # Mop2 = Mop2.reshape((-1,))  #   (n*n) array
        # ediff = ediff.reshape((-1,))  #   (n*n) array

        return ab_eles_arr  # , Mop2, ediff

    def calculate(
        self,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        k_arrs, BZ_bounds = self.kps_in_BZ()

        out_list = MultiCal(self.ab_i, k_arrs, [], core=self.calcoren).calculate()

        out_arr = np.array(out_list)
        # if len(out_arr.shape) == 2:
        #     ab_dist: np.ndarray = out_arr[:, 0]
        #     # Mop2: np.ndarray = out_arr[:, 1]
        #     # ediff: np.ndarray = out_arr[:, 2]
        #     return ab_dist, k_arrs, BZ_bounds

        # print("Absorption matrix shape: ", out_arr.shape)
        # print(
        #     "Size of the absorption matrix: {:.3f} (MB)".format(
        #         sys.getsizeof(out_arr) / 1024**2
        #     ),
        # )
        ab_dist: np.ndarray = out_arr  #   (kpoints, e_range) array
        # Mop2: np.ndarray = out_arr[:, 1, :]  #   (kpoints, n*n) array
        # ediff: np.ndarray = out_arr[:, 2, :]  #   (kpoints, n*n) array
        print("Shape of absorption matrix: ", ab_dist.shape)

        return ab_dist, k_arrs, BZ_bounds


# def main():
#     rcal = RamanCal(ContiTBGHa(2, 1, KM=1), bds_num=5, density=5)
#     rcal.calculate()
#     return


# if __name__ == "__main__":
#     main()
