import numpy as np
from ..pubmeth.consts import *

# from ..pubmeth.pubmeth import HaCo
from typing import Literal
from ..abc.abmoire import (
    ABContiGraMoires,
    ABContiMoHa,
    ABCommGraMoire,
    ABTBHa,
)

# from ..hamiltonians.SK_potential import SKPotential
# from functools import cached_property
import numpy as np

np.seterr(divide="ignore", invalid="ignore")


class SLGHa(ABContiMoHa):
    b_p_arr = np.array([np.sqrt(3) / 2, 1 / 2]) * np.sqrt(3)
    b_n_arr = np.array([-np.sqrt(3) / 2, 1 / 2]) * np.sqrt(3)
    K_b = (b_p_arr + np.array([0, 1]) * np.sqrt(3)) / 3
    K_t = (b_n_arr + np.array([0, 1]) * np.sqrt(3)) / 3
    M = (K_b + K_t) / 2

    def __init__(
        self,
        moInst: ABContiGraMoires,
        signature: Literal["twist_angle", "mat_name"] = "mat_name",
    ) -> None:
        super().__init__(moInst, signature)

        self.a1_arr = self.moInst.a0 * np.array([1 / 2, np.sqrt(3) / 2])
        self.a2_arr = self.moInst.a0 * np.array([-1 / 2, np.sqrt(3) / 2])
        self.delta_arr = (self.a1_arr + self.a2_arr) / 3
        self.t = (
            self.moInst.vF
            * 2
            * h_bar_eV
            * eV2meV
            / (3 * self.moInst.a0 / np.sqrt(3) * A2m)
        )

        self.b_p_arr = self.b_p_arr * self.moInst.K0
        self.b_n_arr = self.b_n_arr * self.moInst.K0
        self.K_b = self.K_b * self.moInst.K0
        self.K_t = self.K_t * self.moInst.K0
        self.M = self.M * self.moInst.K0

    def _h1(self, k_arr):
        pass

    def _h2(self, k_arr):
        pass

    def _hinter(self, k_arr):
        pass

    def h(self, k_arr):
        f_k = np.exp(1j * k_arr @ self.delta_arr) * (
            1 + np.exp(-1j * k_arr @ self.a1_arr) + np.exp(-1j * k_arr @ self.a2_arr)
        )
        h = np.array([[0, -self.t * f_k], [-self.t * np.conj(f_k), 0]])
        return h


class TightTBGHa(ABTBHa):
    def __init__(
        self, commInst: ABCommGraMoire, Vppi0=-2700, Vpps0=480, delta0coeff=0.184
    ) -> None:
        super().__init__(commInst, Vppi0, Vpps0, delta0coeff)


class TightAAtTTGHa(TightTBGHa):
    def __init__(
        self, commInst: ABCommGraMoire, Vppi0=-2700, Vpps0=480, delta0coeff=0.184
    ) -> None:
        super().__init__(commInst, Vppi0, Vpps0, delta0coeff)


class TightAtATTGHa(TightTBGHa):
    def __init__(
        self, commInst: ABCommGraMoire, Vppi0=-2700, Vpps0=480, delta0coeff=0.184
    ) -> None:
        super().__init__(commInst, Vppi0, Vpps0, delta0coeff)


class TightABtTTGHa(TightTBGHa):
    def __init__(
        self, commInst: ABCommGraMoire, Vppi0=-2700, Vpps0=480, delta0coeff=0.184
    ) -> None:
        super().__init__(commInst, Vppi0, Vpps0, delta0coeff)


class TightAtBTTGHa(TightTBGHa):
    def __init__(
        self, commInst: ABCommGraMoire, Vppi0=-2700, Vpps0=480, delta0coeff=0.184
    ) -> None:
        super().__init__(commInst, Vppi0, Vpps0, delta0coeff)


def main():
    a = TightTBGHa()
    a._h1(np.array([0, 0]))
    print(a)

    # a.equal_lats()


if __name__ == "__main__":
    main()
