from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np

# from calcores.hamiltonians.klattices import BiKLattices
from ..hamiltonians.klattices import BiKLattices
from ..pubmeth.consts import *

# from public.consts import *
from typing import Literal, Union

# from calcores.pubmeth.pointset import HexLats
from ..pubmeth.pointset import HexLats

# from calcores.hamiltonians.SK_potential import SKPotential
from ..hamiltonians.SK_potential import SKPotential
from functools import cached_property
import matplotlib.pyplot as plt


class ABContiGraMoires(metaclass=ABCMeta):
    mat_name = "Moire"

    def __init__(
        self,
        twist_angle: float,
        haInst: "ABContiMoHa",
        vFcoeff: float = 1,
        a0: float = 2.46,  #   Angstrom
        kshells: int = 7,
        w_inter=118,
        tperp_coeff=1,
    ) -> None:
        self.a0 = a0
        self.twist_angle = twist_angle
        self.hInst = haInst
        self.vF = 1e6 * vFcoeff
        self.w = w_inter
        self.shells = kshells
        self.tperp_coeff = tperp_coeff
        pass

    @property
    def aM(self):
        sc_period = self.a0 / (2 * np.sin(self.twist_angle / 180 * np.pi / 2))
        return sc_period

    @property
    def renormed_BZ_K_side(self):
        return abs(4 * np.pi / (3 * self.aM))

    @property
    def K0(self):
        return abs(4 * np.pi / (3 * self.a0))

    @property
    def areaM(self):
        return np.sqrt(3) / 2 * self.aM**2

    @property
    def areaO(self):
        return np.sqrt(3) / 2 * self.a0**2

    @property
    def epsilonM(self):
        return h_bar_eV * self.vF * self.renormed_BZ_K_side * m2A * eV2meV

    @property
    def epsilonO(self):
        return h_bar_eV * self.vF * self.K0 * m2A * eV2meV


class ABContiMoHa(metaclass=ABCMeta):
    b_p_arr = np.array([np.sqrt(3) / 2, 3 / 2])
    b_n_arr = np.array([-np.sqrt(3) / 2, 3 / 2])
    K_b = np.array([-np.sqrt(3) / 2, -1 / 2])
    K_t = np.array([-np.sqrt(3) / 2, 1 / 2])
    Gamma = np.array([0, 0])
    M = (K_b + K_t) / 2
    BZ_renormed = True

    def __init__(
        self,
        moInst: "ABContiGraMoires",
        signature: Literal["twist_angle", "mat_name"] = "twist_angle",
    ) -> None:
        self.moInst = moInst
        self.k1, self.k2 = BiKLattices(self.moInst.shells).basis_set()
        self.expand_v = BiKLattices(self.moInst.shells).expand_vecs()
        self.sigs = getattr(self.moInst, signature)
        if isinstance(self.sigs, float):
            self.sigs = "{:.2f}".format(self.sigs)
        pass

    @abstractmethod
    def _h1(self, k_arr):
        pass

    @abstractmethod
    def _h2(self, k_arr):
        pass

    @abstractmethod
    def _hinter(self, k_arr):
        pass

    @abstractmethod
    def h(self, k_arr):
        pass


class ABCommGraMoire(metaclass=ABCMeta):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: "ABTBHa",
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        self.m0 = m0
        self.r = r
        self.a1 = a0 * a1
        self.a2 = a0 * a2

        self.hInst = haInst

        self.twist_angle = round(
            (
                np.arccos(
                    (3 * m0**2 + 3 * m0 * r + r**2 / 2)
                    / (3 * m0**2 + 3 * m0 * r + r**2)
                )
                / pi
                * 180
            ),
            2,
        )

        self.mat_name = "{:.2f} Commensurate Moire".format(self.twist_angle)

        self.a0 = a0
        self.d = 3.35

        self.scale = int(np.linalg.norm(self.R1) // np.linalg.norm(self.a1) * 2)

        self.inv_mat = np.linalg.inv(
            np.array(
                [
                    [np.linalg.norm(self.R1) ** 2, self.R1 @ self.R2],
                    [self.R1 @ self.R2, np.linalg.norm(self.R1) ** 2],
                ]
            )
        )

    @property
    def aM(self):
        return self.a0 / (2 * np.sin(self.twist_angle / 180 * np.pi / 2))

    @property
    def areaM(self):
        return np.sqrt(3) / 2 * self.aM**2

    @property
    def renormed_BZ_K_side(self):
        return 1

    @property
    def R1(self):
        R1 = (
            self.m0 * self.a1 + (self.m0 + self.r) * self.a2
            if self.r % 3 != 0
            else (self.m0 + (self.r // 3)) * self.a1 + (self.r // 3) * self.a2
        )
        return R1

    @property
    def R2(self):
        R2 = (
            -(self.m0 + self.r) * self.a1 + (2 * self.m0 + self.r) * self.a2
            if self.r % 3 != 0
            else -(self.r // 3) * self.a1 + (self.m0 + 2 * (self.r // 3)) * self.a2
        )
        return R2

    @property
    @abstractmethod
    def lat1(self):
        pass

    @property
    @abstractmethod
    def lat2(self):
        pass

    @property
    @abstractmethod
    def lindexes(self):
        pass

    def lats_transf(self, r_angle=0, shift_arr=np.array([0, 0])):
        return HexLats(
            self.a1,
            self.a2,
            density_tuple=(self.scale, self.scale),
            r_angle=r_angle,
            shift_arr=shift_arr,
        ).basis_change(self.inv_mat, self.R1, self.R2)

    def _getlatswithin(self, lat_i: Literal["0", "1", "2", "3"] = "1"):
        lats = getattr(self, "lat{}".format(lat_i))
        cond1 = np.logical_and(lats[:, 0] < 0.5, lats[:, 0] >= -0.5)
        cond2 = np.logical_and(lats[:, 1] < 0.5, lats[:, 1] >= -0.5)
        # cond1 = np.logical_and(lats[:, 0] < 1, lats[:, 0] >= 0)
        # cond2 = np.logical_and(lats[:, 1] < 1, lats[:, 1] >= 0)
        cond = np.logical_and(cond1, cond2)
        return lats[cond]

    def atoms_rvec(
        self, lat_i: Union[Literal[0, 1, 2, 3, "within"], np.ndarray] = 1, zdefault=0
    ):
        if isinstance(lat_i, int):
            lats = getattr(self, "lat{}".format(lat_i))
            z = (int(lat_i) - 1) * self.d * np.ones((len(lats), 1))
        elif isinstance(lat_i, np.ndarray):
            if len(lat_i.shape) == 1:
                lats = lat_i.reshape((1, -1))
                z = zdefault * np.ones((len(lats), 1))
            elif len(lat_i.shape) > 1 and lat_i.shape[0] > 1:
                lats = lat_i
                zi = (np.array(self.lindexes) - 1).reshape((-1, 1))
                z = np.kron(zi, np.ones((len(lats) // len(self.lindexes), 1))) * self.d
        elif lat_i == "within":
            lats = getattr(self, "latwithin")
            zi = (np.array(self.lindexes) - 1).reshape((-1, 1))
            z = np.kron(zi, np.ones((len(lats) // len(self.lindexes), 1))) * self.d
        xy_pos = np.kron(lats[:, 0].reshape((-1, 1)), self.R1) + np.kron(
            lats[:, 1].reshape((-1, 1)), self.R2
        )
        return np.hstack([xy_pos, z])

    @cached_property
    def latwithin(self):
        return np.vstack([self._getlatswithin("{}".format(i)) for i in self.lindexes])

    @property
    def expand_basis(self):
        return np.array(
            [
                [0, 0],
                [0, 1],
                [0, -1],
                [1, 0],
                [-1, 0],
                [1, 1],
                [1, -1],
                [-1, 1],
                [-1, -1],
            ]
        )

    def equal_rvecs(self):
        expand_vecs = np.kron(np.ones((len(self.latwithin), 1)), self.expand_basis)
        olats = np.kron(self.latwithin, np.ones((len(self.expand_basis), 1)))
        exlats = expand_vecs + olats
        rvecs = self.atoms_rvec(exlats)
        return rvecs


class ABTBHa(ABContiMoHa, metaclass=ABCMeta):
    BZ_renormed = False

    def __init__(
        self,
        commInst: "ABCommGraMoire",
        Vppi0=-2700,
        Vpps0=480,
        delta0coeff=0.184,
    ) -> None:
        self.moInst = commInst

        self.sigs = self.moInst.twist_angle

        a1z = np.hstack([self.moInst.a1, np.zeros((1,))])
        a2z = np.hstack([self.moInst.a2, np.zeros((1,))])
        a3z = np.array([0, 0, 1])
        self.b1 = 2 * pi * (np.cross(a2z, a3z)) / (a1z @ np.cross(a2z, a3z))
        self.b2 = 2 * pi * (np.cross(a3z, a1z)) / (a1z @ np.cross(a2z, a3z))

        self.b_p_arr = (
            (
                (2 * self.moInst.m0 + self.moInst.r) * self.b1
                + (self.moInst.m0 + self.moInst.r) * self.b2
            )
            / (
                3 * self.moInst.m0**2
                + 3 * self.moInst.m0 * self.moInst.r
                + self.moInst.r**2
            )
            if self.moInst.r % 3 != 0
            else (
                (self.moInst.m0 + 2 * (self.moInst.r // 3)) * self.b1
                + (self.moInst.r // 3) * self.b2
            )
            / (
                self.moInst.m0**2
                + self.moInst.m0 * self.moInst.r
                + self.moInst.r**2 / 3
            )
        )

        self.b_n_arr = (
            (-(self.moInst.m0 + self.moInst.r) * self.b1 + self.moInst.m0 * self.b2)
            / (
                3 * self.moInst.m0**2
                + 3 * self.moInst.m0 * self.moInst.r
                + self.moInst.r**2
            )
            if self.moInst.r % 3 != 0
            else (
                -(self.moInst.r // 3) * self.b1
                + (self.moInst.m0 + (self.moInst.r // 3)) * self.b2
            )
            / (
                self.moInst.m0**2
                + self.moInst.m0 * self.moInst.r
                + self.moInst.r**2 / 3
            )
        )
        self.K_b = ((self.b_p_arr + 2 * self.b_n_arr) / 3)[:2]
        self.K_t = ((2 * self.b_p_arr + self.b_n_arr) / 3)[:2]
        self.M = (self.K_b + self.K_t) / 2

        self.skp = SKPotential(
            Vppi0=Vppi0,
            Vpps0=Vpps0,
            a0=self.moInst.a0 / np.sqrt(3),
            d0=self.moInst.d,
            delta0=delta0coeff * self.moInst.a0,
        )

    @cached_property
    def equal_distarrs(self) -> np.ndarray:
        olats = self.moInst.atoms_rvec("within")
        explats = self.moInst.equal_rvecs()
        olats_e: np.ndarray = np.kron(olats, np.ones((len(explats), 1)))
        explats_e: np.ndarray = np.kron(np.ones((len(olats), 1)), explats)

        dist_arrs = explats_e - olats_e

        return dist_arrs

    @cached_property
    def equal_cos(self) -> np.ndarray:
        cos_arrs: np.ndarray = self.equal_distarrs[:, -1] / np.linalg.norm(
            self.equal_distarrs, axis=1
        )
        cos_arrs[np.isnan(cos_arrs)] = 0
        return cos_arrs

    @cached_property
    def equal_vppi(self) -> np.ndarray:
        return self.skp.Vppi(np.linalg.norm(self.equal_distarrs, axis=1))

    @cached_property
    def equal_vpps(self) -> np.ndarray:
        return self.skp.Vpps(np.linalg.norm(self.equal_distarrs, axis=1))

    def h(self, k_arr):
        equal_cos = self.equal_cos.reshape((-1, len(self.moInst.expand_basis))).T
        equal_vppi = self.equal_vppi.reshape((-1, len(self.moInst.expand_basis))).T
        equal_vpps = self.equal_vpps.reshape((-1, len(self.moInst.expand_basis))).T
        phase_term: np.ndarray = np.exp(1j * k_arr @ self.equal_distarrs[:, :2].T)
        phase_term = phase_term.reshape(-1, len(self.moInst.expand_basis)).T
        h = phase_term * (equal_vppi * (1 - equal_cos**2) + equal_vpps * equal_cos**2)
        h: np.ndarray = np.sum(h, axis=0)
        h = h.reshape((len(self.moInst.latwithin), len(self.moInst.latwithin)))

        return h

    def _h2(self, k_arr):
        pass

    def _h1(self, k_arr):
        pass

    def _hinter(self, k_arr):
        pass


def main():
    return


if __name__ == "__main__":
    main()
