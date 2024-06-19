from ..hamiltonians.conti_h import ContiTBGHa
import numpy as np
from ..hamiltonians.tb_h import TightTBGHa
from ..multical.multicorecal import MultiCal
from ..filesop.filesave import FilesSave
from ..abc.abmoire import ABContiMoHa
from typing import Union


class BandsCal:
    def __init__(
        self,
        haInst: Union[ABContiMoHa, TightTBGHa],
        p_density=100,
        path: Union[list[str], list[np.ndarray]] = ["K_b", "M", "Gamma", "K_t"],
        suffix="",
    ) -> None:
        self.haInst: Union[ABContiMoHa, TightTBGHa] = haInst
        self.p_density = p_density
        self.path = path

        self.fname = (
            self.haInst.__class__.__name__
            + "_{}".format(self.haInst.sigs)
            + "{}".format(suffix)
        )
        pass

    def _set_points(self):
        path_arr_list = []
        last_p = None
        p_num_list = [0]
        for ele_point_i in range(len(self.path) - 1):
            p2 = (
                getattr(self.haInst, self.path[ele_point_i + 1])
                if isinstance(self.path[ele_point_i + 1], str)
                else self.path[ele_point_i + 1]
            )
            p1 = (
                getattr(self.haInst, self.path[ele_point_i])
                if isinstance(self.path[ele_point_i], str)
                else self.path[ele_point_i]
            )
            dist = np.linalg.norm(p2 - p1)
            p_num = int(self.p_density * dist)
            p_num_list.append(p_num + p_num_list[-1])
            for ele_i in np.linspace(0, 1, p_num, endpoint=False):
                path_arr_list.append(p1 + ele_i * (p2 - p1))
            last_p = p2

        ### Include the last k point
        path_arr_list.append(last_p)
        return path_arr_list, p_num_list

    def eigenvalues(self, k_arr):
        eig_values = np.linalg.eig(self.haInst.h(k_arr))[0]
        eig_values.sort()
        return eig_values

    def calculate(self) -> tuple[np.ndarray, list[int]]:
        arr_list, xlabel_x = self._set_points()
        cal = MultiCal(self.eigenvalues, arr_list, [])
        path_energies = cal.calculate()
        return np.real(path_energies), xlabel_x


def main():
    BandsCal(ContiTBGHa(1, epsilon=1)).calculate()
    return


if __name__ == "__main__":
    main()
