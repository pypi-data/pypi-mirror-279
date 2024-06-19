from ..abc.abmoire import ABContiGraMoires, ABCommGraMoire, np
from ..abc.abcal import ABCal
from functools import cached_property


class HamOut:
    """
    Used to output all the Hamiltonian over the Brillouin zone from twisted graphene classes, including continuum model and commensurate model.

    However, note that for continuum model, the dimension of the Hamiltonian matrix will increase once k_shell parameters (within continuum model class) are set to be larger (default 7).

    Therefore, the density parameter in this class should not be rather large for the continuum model.
    """

    def __init__(
        self, moInst: ABContiGraMoires | ABCommGraMoire, density=70, core_num=3
    ) -> None:
        self.moInst = moInst

        self.density = density
        self.core_num = core_num

    @property
    def _abCalInst(self):
        """
        Abstract calculation instance. Used to generate the k arrays in the Brillouin zone
        """
        return ABCal(self.moInst.hInst, self.density, self.core_num)

    def HamOverBZ(self):
        """
        return: k_arr, h_matrix_arr, eig_vals_arr, eig_vecs_arr
        """
        k_arrs = self._abCalInst.kps_in_BZ()[0]
        h_list = []

        eig_vals_list = []
        eig_vecs_list = []

        for ele_karr in k_arrs:
            ele_h = self.moInst.hInst(self.moInst).h(ele_karr)

            eig_vals, eig_vecs = np.linalg.eig(ele_h)

            h_list.append(ele_h)
            eig_vals_list.append(eig_vals)
            eig_vecs_list.append(eig_vecs)

        h_arr = np.array(h_list)
        eig_vals_arr = np.array(eig_vals_list)
        eig_vecs_arr = np.array(eig_vecs_list)

        return k_arrs, h_arr, eig_vals_arr, eig_vecs_arr
