from ..abc.abmoire import ABContiMoHa
import numpy as np


class VelocityOperator:
    def __init__(self, hInst: ABContiMoHa, ki=0.005, bds_num=5) -> None:
        self.hInst = hInst
        self.ki = ki
        self.bds_num = bds_num

    def calculate(self, k_arr):
        hc = self.hInst.h(k_arr)
        hxd = (self.hInst.h(k_arr + np.array([self.ki, 0])) - hc) / (
            self.ki * self.hInst.moInst.renormed_BZ_K_side
        )
        hyd = (self.hInst.h(k_arr + np.array([0, self.ki])) - hc) / (
            self.ki * self.hInst.moInst.renormed_BZ_K_side
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

        ediff: np.ndarray = np.kron(
            c_energy_arr.reshape((-1, 1)), np.ones((1, bds_num))
        ) - np.kron(np.ones((bds_num, 1)), v_energy_arr.reshape((1, -1)))

        return hx, hy, ediff
