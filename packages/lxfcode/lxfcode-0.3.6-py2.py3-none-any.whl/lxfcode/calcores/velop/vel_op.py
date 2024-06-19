from ..abc.abmoire import ABContiMoHa
from ..hamiltonians.conti_h import ContiTBGHa
import numpy as np
from ..multical.multicorecal import MultiCal
from ..abc.abcal import ABCal


class VelOp:
    def __init__(self, hInst: ABContiMoHa, k_interval=1e-4) -> None:
        self.hInst: ABContiMoHa = hInst
        self.k_i = k_interval

    def hc(self, k_arr):
        hc = self.hInst.h(k_arr)
        return hc

    # def hxd(self, k_arr):
    #     if self.hInst.BZ_renormed:

    #     return

    def sigma_xx(self):
        return
