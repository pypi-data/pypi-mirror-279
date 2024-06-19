from abc import ABCMeta, abstractmethod

# from calcores.abc.abmoire import ABMoHa, np
from .abmoire import ABContiMoHa
import numpy as np


class ABCal(metaclass=ABCMeta):
    def __init__(
        self, haInst: ABContiMoHa, density: int = 70, cal_corenum: int = 3
    ) -> None:
        self.haInst = haInst
        self.density = density
        self.calcoren = cal_corenum
        pass

    def kps_in_BZ(self):
        b1 = self.haInst.b_n_arr[:2]
        b2 = self.haInst.b_p_arr[:2]

        coeff_arr = np.linspace(0, 1, self.density, endpoint=False).reshape((-1, 1))

        b1e: np.ndarray = np.kron(coeff_arr * b1, np.ones((self.density, 1)))

        b2e: np.ndarray = np.kron(np.ones((self.density, 1)), coeff_arr * b2)

        k_arrs = b1e + b2e

        boundaries = [self.haInst.Gamma, b1, b1 + b2, b2, self.haInst.Gamma]
        boundaries = [vec[:2] for vec in boundaries]

        return k_arrs, np.array(boundaries)
