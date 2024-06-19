import numpy as np
from ..pubmeth.consts import *
from ..pubmeth.pubmeth import HaCo
from ..abc.abmoire import ABContiGraMoires, ABContiMoHa


class ContiTBGHa(ABContiMoHa):
    def __init__(self, moInst: ABContiGraMoires) -> None:
        super().__init__(moInst)

    def _h1(self, k_arr):
        a = np.kron(self.k1[:, 0].reshape((-1, 1)), self.b_p_arr)
        b = np.kron(self.k1[:, 1].reshape((-1, 1)), self.b_n_arr)
        c = np.kron(np.ones((len(self.k1[:, 0]), 1)), self.K_b)

        return (
            HaCo.DiracH(a + b - c + k_arr, self.moInst.twist_angle / 2)
            * self.moInst.epsilonM
        )

    def _h2(self, k_arr):
        a = np.kron(self.k2[:, 0].reshape((-1, 1)), self.b_p_arr)
        b = np.kron(self.k2[:, 1].reshape((-1, 1)), self.b_n_arr)
        c = np.kron(np.ones((len(self.k2[:, 0]), 1)), self.K_t)
        return (
            HaCo.DiracH(a + b - c + k_arr, -self.moInst.twist_angle / 2)
            * self.moInst.epsilonM
        )

    def _hinter(self):
        """
        Interlayer coupling
        """
        k1e = np.kron(self.k1, np.ones((len(self.k2), 1)))
        k2e = np.kron(np.ones((len(self.k1), 1)), self.k2)
        diff_k = k2e - k1e
        x = diff_k[:, 0]
        y = diff_k[:, 1]
        j1 = np.logical_and(x == 0, y == 0)
        j2 = np.logical_and(x == 1, y == 0)
        j3 = np.logical_and(x == 0, y == 1)

        inter_T = [
            self.moInst.w * np.ones((2, 2)),
            self.moInst.w
            * np.array([[1, np.exp(-2j * pi / 3)], [np.exp(2j * pi / 3), 1]]),
            self.moInst.w
            * np.array([[1, np.exp(2j * pi / 3)], [np.exp(-2j * pi / 3), 1]]),
        ]
        j_list = [j1, j2, j3]

        inter_mat = np.zeros((len(self.k1) * 2, len(self.k2) * 2)) + 0j
        for ele_couple_i in np.arange(len(j_list)):
            row_i = np.where(j_list[ele_couple_i] == True)[0] // len(self.k2) * 2
            col_i = np.where(j_list[ele_couple_i] == True)[0] % len(self.k2) * 2
            for ele_i in range(len(row_i)):
                inter_mat[
                    row_i[ele_i] : row_i[ele_i] + 2, col_i[ele_i] : col_i[ele_i] + 2
                ] = inter_T[ele_couple_i]
        return inter_mat

    def h(self, k_arr):
        h11 = self._h1(k_arr)
        h22 = self._h2(k_arr)
        hi = self._hinter()

        out_mat = np.block([[h11, hi], [np.conj(hi.T), h22]])

        return out_mat


class EffABtHa(ContiTBGHa):
    def __init__(self, moInst: ABContiGraMoires) -> None:
        super().__init__(moInst)

    def _h1(self, k_arr):
        a = np.kron(self.k1[:, 0].reshape((-1, 1)), self.b_p_arr)
        b = np.kron(self.k1[:, 1].reshape((-1, 1)), self.b_n_arr)
        c = np.kron(np.ones((len(self.k1[:, 0]), 1)), self.K_b)
        return (
            HaCo.ParabH(
                a + b - c + k_arr,
                self.moInst.twist_angle / 2,
                epsilon=self.moInst.epsilonM,
                tperp=357 * self.moInst.tperp_coeff,
            )
            * self.moInst.epsilonM
        )

    def _hinter(self):
        """
        Interlayer coupling
        """
        k1e = np.kron(self.k1, np.ones((len(self.k2), 1)))
        k2e = np.kron(np.ones((len(self.k1), 1)), self.k2)
        diff_k = k2e - k1e
        x = diff_k[:, 0]
        y = diff_k[:, 1]
        j1 = np.logical_and(x == 0, y == 0)
        j2 = np.logical_and(x == 1, y == 0)
        j3 = np.logical_and(x == 0, y == 1)

        inter_T = [
            self.moInst.w * np.ones((2, 2)),
            self.moInst.w
            * np.array([[1, np.exp(-2j * pi / 3)], [np.exp(2j * pi / 3), 1]]),
            self.moInst.w
            * np.array([[1, np.exp(2j * pi / 3)], [np.exp(-2j * pi / 3), 1]]),
        ]
        inter_T = [np.vstack([np.zeros((2, 2)), ele]) for ele in inter_T]
        j_list = [j1, j2, j3]

        inter_mat = np.zeros((len(self.k1) * 4, len(self.k2) * 2)) + 0j

        for ele_couple_i in np.arange(len(j_list)):
            row_i = np.where(j_list[ele_couple_i] == True)[0] // len(self.k2) * 4
            col_i = np.where(j_list[ele_couple_i] == True)[0] % len(self.k2) * 2
            for ele_i in range(len(row_i)):
                inter_mat[
                    row_i[ele_i] : row_i[ele_i] + 4, col_i[ele_i] : col_i[ele_i] + 2
                ] = inter_T[ele_couple_i]
        return inter_mat


class EffAtAHa(ContiTBGHa):
    def __init__(self, moInst: ABContiGraMoires) -> None:
        super().__init__(moInst)

    def _h1(self, k_arr):
        a = np.kron(self.k1[:, 0].reshape((-1, 1)), self.b_p_arr)
        b = np.kron(self.k1[:, 1].reshape((-1, 1)), self.b_n_arr)
        c = np.kron(np.ones((len(self.k1[:, 0]), 1)), self.K_b)
        return (
            HaCo.AAstackedH(
                a + b - c + k_arr,
                self.moInst.twist_angle / 2,
                epsilon=self.moInst.epsilonM,
                tperp_AA=4,
                tperp_BB=4,
            )
            * self.moInst.epsilonM
        )

    def _hinter(self):
        """
        AtA Interlayer coupling
        """
        k1e = np.kron(self.k1, np.ones((len(self.k2), 1)))
        k2e = np.kron(np.ones((len(self.k1), 1)), self.k2)
        diff_k = k2e - k1e
        x = diff_k[:, 0]
        y = diff_k[:, 1]
        j1 = np.logical_and(x == 0, y == 0)
        j2 = np.logical_and(x == 1, y == 0)
        j3 = np.logical_and(x == 0, y == 1)

        inter_T = [
            self.moInst.w * np.ones((2, 2)),
            self.moInst.w
            * np.array([[1, np.exp(-2j * pi / 3)], [np.exp(2j * pi / 3), 1]]),
            self.moInst.w
            * np.array([[1, np.exp(2j * pi / 3)], [np.exp(-2j * pi / 3), 1]]),
        ]
        inter_T = [np.vstack([ele] * 2) for ele in inter_T]
        j_list = [j1, j2, j3]

        inter_mat = np.zeros((len(self.k1) * 4, len(self.k2) * 2)) + 0j

        for ele_couple_i in np.arange(len(j_list)):
            row_i = np.where(j_list[ele_couple_i] == True)[0] // len(self.k2) * 4
            col_i = np.where(j_list[ele_couple_i] == True)[0] % len(self.k2) * 2
            for ele_i in range(len(row_i)):
                inter_mat[
                    row_i[ele_i] : row_i[ele_i] + 4, col_i[ele_i] : col_i[ele_i] + 2
                ] = inter_T[ele_couple_i]
        return inter_mat


class EffAtBHa(ContiTBGHa):
    def __init__(self, moInst: ABContiGraMoires) -> None:
        super().__init__(moInst)

    def _h1(self, k_arr):
        a = np.kron(self.k1[:, 0].reshape((-1, 1)), self.b_p_arr)
        b = np.kron(self.k1[:, 1].reshape((-1, 1)), self.b_n_arr)
        c = np.kron(np.ones((len(self.k1[:, 0]), 1)), self.K_b)
        return (
            HaCo.ParabH(
                a + b - c + k_arr,
                self.moInst.twist_angle / 2,
                epsilon=self.moInst.epsilonM,
                tperp=2,
            )
            * self.moInst.epsilonM
        )

    def _hinter(self):
        """
        AtA Interlayer coupling
        """
        k1e = np.kron(self.k1, np.ones((len(self.k2), 1)))
        k2e = np.kron(np.ones((len(self.k1), 1)), self.k2)
        diff_k = k2e - k1e
        x = diff_k[:, 0]
        y = diff_k[:, 1]
        j1 = np.logical_and(x == 0, y == 0)
        j2 = np.logical_and(x == 1, y == 0)
        j3 = np.logical_and(x == 0, y == 1)

        inter_T = [
            self.moInst.w * np.ones((2, 2)),
            self.moInst.w
            * np.array([[1, np.exp(-2j * pi / 3)], [np.exp(2j * pi / 3), 1]]),
            self.moInst.w
            * np.array([[1, np.exp(2j * pi / 3)], [np.exp(-2j * pi / 3), 1]]),
        ]
        inter_T = [np.vstack([ele * np.exp(2j * pi / 3), ele]) for ele in inter_T]
        j_list = [j1, j2, j3]

        inter_mat = np.zeros((len(self.k1) * 4, len(self.k2) * 2)) + 0j

        for ele_couple_i in np.arange(len(j_list)):
            row_i = np.where(j_list[ele_couple_i] == True)[0] // len(self.k2) * 4
            col_i = np.where(j_list[ele_couple_i] == True)[0] % len(self.k2) * 2
            for ele_i in range(len(row_i)):
                inter_mat[
                    row_i[ele_i] : row_i[ele_i] + 4, col_i[ele_i] : col_i[ele_i] + 2
                ] = inter_T[ele_couple_i]
        return inter_mat


def main():
    # h = EffABtHa(1, 1, shells=1).h(np.array([1, 1]))
    # print(h.shape)
    arrs = []
    for ele_px in np.linspace(-1, 1, 200):
        arrs.append(np.array([ele_px, 0]))

    H1 = HaCo.ParabH(np.array(arrs), 0, 1)

    pass


if __name__ == "__main__":
    main()
