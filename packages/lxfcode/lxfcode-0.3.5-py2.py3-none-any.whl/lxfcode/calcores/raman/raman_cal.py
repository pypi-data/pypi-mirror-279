from ..abc.abmoire import ABContiMoHa
from ..hamiltonians.conti_h import ContiTBGHa
import numpy as np
from ..multical.multicorecal import MultiCal
from ..abc.abcal import ABCal


class RamanCal(ABCal):
    def __init__(
        self,
        haInst: ABContiMoHa,
        density: int = 70,
        cal_corenum: int = 3,
        e_photon=2330,
        interval_k=0.005,
        bds_num: int = 5,
        gamma=100,
        e_phonon=196,
    ) -> None:
        super().__init__(haInst, density, cal_corenum)

        self.e_op = e_photon
        self.bds_num = bds_num
        self.ki = interval_k
        self.gamma = gamma
        self.e_ph = e_phonon

    def raman_i(self, k_arr):
        hc = self.haInst.h(k_arr)
        hxd = (self.haInst.h(k_arr + np.array([self.ki, 0])) - hc) / (
            self.ki * self.haInst.moInst.renormed_BZ_K_side
        )
        hyd = (self.haInst.h(k_arr + np.array([0, self.ki])) - hc) / (
            self.ki * self.haInst.moInst.renormed_BZ_K_side
        )

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
        ) - np.kron(np.ones((bds_num, 1)), v_energy_arr.reshape((1, -1)))

        raman_eles: np.ndarray = Mop2 / (
            (self.e_op - np.array(ediff) - 1j * self.gamma)
            * (self.e_op - np.array(ediff) - self.e_ph - 1j * self.gamma)
        )

        raman_eles = raman_eles.reshape((-1,))
        Mop2 = Mop2.reshape((-1,))
        ediff = ediff.reshape((-1,))

        return raman_eles, Mop2, ediff

    def calculate(
        self,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        k_arrs, BZ_bounds = self.kps_in_BZ()

        out_list = MultiCal(self.raman_i, k_arrs, [], core=self.calcoren).calculate()

        out_arr = np.array(out_list)
        if len(out_arr.shape) == 2:
            raman_dist: np.ndarray = out_arr[:, 0]
            Mop2: np.ndarray = out_arr[:, 1]
            ediff: np.ndarray = out_arr[:, 2]
            return raman_dist, Mop2, np.real(ediff), k_arrs, BZ_bounds

        raman_dist: np.ndarray = out_arr[:, 0, :]
        Mop2: np.ndarray = out_arr[:, 1, :]
        ediff: np.ndarray = out_arr[:, 2, :]

        return raman_dist, Mop2, np.real(ediff), k_arrs, BZ_bounds


def main():
    rcal = RamanCal(ContiTBGHa(2, 1, KM=1), bds_num=5, density=5)
    rcal.calculate()
    return


if __name__ == "__main__":
    main()
