from ..abc.abmoire import ABCommGraMoire, ABTBHa
from functools import cached_property

# from ..hamiltonians.tb_h import TightTBGHa
import numpy as np
from ..pubmeth.pointset import HexLats

np.seterr(divide="ignore", invalid="ignore")


class CommTBGStru(ABCommGraMoire):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)

    @property
    def lindexes(self):
        return [1, 2]

    @cached_property
    def lat1(self):
        return self.lats_transf(r_angle=0)

    @cached_property
    def lat2(self):
        return self.lats_transf(r_angle=self.twist_angle)


class CommAAtTTGStru(CommTBGStru):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)

    @property
    def lindexes(self):
        return [0, 1, 2]

    @property
    def lat0(self):
        return self.lats_transf(r_angle=0)


class CommAtATTGStru(CommAAtTTGStru):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)

    @property
    def lindexes(self):
        return [1, 2, 3]

    @property
    def lat3(self):
        return self.lats_transf(r_angle=0)


class CommABtTTGStru(CommAAtTTGStru):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)

    @property
    def lat0(self):
        return self.lats_transf(r_angle=0, shift_arr=HexLats(self.a1, self.a2).d_arr)


class CommAtBTTGStru(CommAtATTGStru):
    def __init__(
        self,
        m0: int,
        r: int,
        haInst: ABTBHa,
        a1: np.ndarray = np.array([np.sqrt(3) / 2, -1 / 2]),
        a2: np.ndarray = np.array([np.sqrt(3) / 2, 1 / 2]),
        a0: float = 2.46,
    ) -> None:
        super().__init__(m0, r, haInst, a1, a2, a0)

    @property
    def lat3(self):
        return self.lats_transf(r_angle=0, shift_arr=HexLats(self.a1, self.a2).d_arr)


def main():
    a = CommAAtTTGStru(1, 1)
    rvecs = a.atoms_rvec("within")
    pass


if __name__ == "__main__":
    main()
