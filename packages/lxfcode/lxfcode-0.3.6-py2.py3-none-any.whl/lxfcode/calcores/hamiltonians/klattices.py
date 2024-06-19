import numpy as np


class BiKLattices:
    def __init__(self, shells=7, twist_layer=2, res_layer=None) -> None:
        self.shells = shells
        self.twist_layer = twist_layer
        self.res_layer = res_layer
        pass

    def expand_vecs(self):
        twist_diff = self.twist_layer - 1
        expand_v = np.array(
            [[0, 0, twist_diff], [1, 0, twist_diff], [0, 1, twist_diff]]
        )
        return expand_v

    def basis_set(self):
        v0 = np.array([[0, 0, 1]])
        v1_list = [v0]
        v2_list = []
        expand_v = self.expand_vecs()
        to_v1 = False
        while self.shells > 0:
            self.shells -= 1
            if to_v1:
                tmp_vecs = np.kron(v2_list[-1], np.ones((3, 1))) - np.kron(
                    np.ones((len(v2_list[-1]), 1)), expand_v
                )

                tmp_vecs = np.unique(tmp_vecs, axis=0)
                v1_list.append(tmp_vecs)
            else:
                tmp_vecs = np.kron(v1_list[-1], np.ones((3, 1))) + np.kron(
                    np.ones((len(v1_list[-1]), 1)), expand_v
                )

                tmp_vecs = np.unique(tmp_vecs, axis=0)
                v2_list.append(tmp_vecs)
            to_v1 = not to_v1
        v1_list = np.unique(np.vstack(v1_list), axis=0)
        v2_list = np.unique(np.vstack(v2_list), axis=0)

        if not (self.res_layer is None):
            res_diff = self.res_layer - 1
            v3_list = v1_list.copy()
            v3_list[:, -1] += res_diff
            return v1_list, v2_list, v3_list

        return v1_list, v2_list


class TriKLattices(BiKLattices):
    def __init__(self, shells=7, twist_layer=2, res_layer=None) -> None:
        super().__init__(shells, twist_layer, res_layer)
        self.res_layer = 3 if twist_layer == 2 else 2
