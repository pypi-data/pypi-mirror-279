import numpy as np
import matplotlib.pyplot as plt
from .pubmeth import PubMethod


class TriLats:
    def __init__(
        self,
        a1: np.ndarray,
        a2: np.ndarray,
        density_tuple: tuple = (15, 15),
        shift_arr: np.ndarray = np.array([0, 0]),
    ) -> None:
        self.a1 = a1
        self.a2 = a2
        self.shift_arr = shift_arr

        self.density_tuple = density_tuple

    @property
    def points(self) -> np.ndarray:
        xm, ym = np.meshgrid(
            np.arange(-self.density_tuple[0], self.density_tuple[0]),
            np.arange(-self.density_tuple[1], self.density_tuple[1]),
        )
        xm = xm.reshape((-1, 1))
        ym = ym.reshape((-1, 1))
        return xm * self.a1 + ym * self.a2 + self.shift_arr

    def __getitem__(self, key):
        return self.points[key]


class HexLats:
    def __init__(
        self,
        a1: np.ndarray,
        a2: np.ndarray,
        density_tuple: tuple = (15, 15),
        r_angle=0,
        shift_arr=np.array([0, 0]),
    ) -> None:
        self.a1 = a1
        self.a2 = a2
        self.density_tuple = density_tuple

        self.r_angle = r_angle
        self.shift_arr = shift_arr

        if a1 @ a2 < 0:
            self.d_arr = (a1 - a2) / 3
        elif a1 @ a2 > 0:
            self.d_arr = (a1 + a2) / 3

    @property
    def lat1(self):
        return TriLats(self.a1, self.a2, self.density_tuple)

    @property
    def lat2(self):
        return TriLats(self.a1, self.a2, self.density_tuple, shift_arr=self.d_arr)

    def __getitem__(self, key):
        all_lats = (
            np.transpose(
                PubMethod.r_mat(self.r_angle)
                @ np.vstack([self.lat1[:], self.lat2[:]]).T
            )
            + self.shift_arr
        )
        return all_lats[key]

    def basis_change(self, mat: np.ndarray, r1: np.ndarray, r2: np.ndarray):
        lats: np.ndarray = self[:] @ np.hstack(
            [r1.reshape((-1, 1)), r2.reshape((-1, 1))]
        )

        return np.transpose(mat @ lats.T)


def main():
    b = HexLats(
        np.array([np.sqrt(3) / 2, 1 / 2]),
        np.array([-np.sqrt(3) / 2, 1 / 2]),
        density_tuple=(10, 10),
    )
    fig, ax = plt.subplots()
    ax.scatter(b[:, 0], b[:, 1], marker=".")
    ax.set_aspect("equal")
    ax.set_xlabel("", fontsize=12)
    ax.set_ylabel("", fontsize=12)
    ax.set_title("", fontsize=14)
    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(ax.get_ylim())
    ax.legend([])
    fig.savefig("tmp.png", dpi=330, facecolor="w", bbox_inches="tight", pad_inches=0.1)
    fig.savefig("tmp.pdf", dpi=330, facecolor="w", bbox_inches="tight", pad_inches=0.1)
    plt.close()


if __name__ == "__main__":
    main()
