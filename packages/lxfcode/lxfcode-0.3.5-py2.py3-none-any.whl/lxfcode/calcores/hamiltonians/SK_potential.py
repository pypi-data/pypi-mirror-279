from typing import Union
import numpy as np
import matplotlib.pyplot as plt


class SKPotential:
    def __init__(self, Vppi0, Vpps0, a0, d0, delta0) -> None:
        self.Vppi0 = Vppi0
        self.Vpps0 = Vpps0

        self.a0 = a0
        self.d0 = d0
        self.delta0 = delta0

    def Vppi(self, d: Union[float, np.ndarray]):
        return self.Vppi0 * np.exp(-((d - self.a0) / self.delta0))

    def Vpps(self, d: Union[float, np.ndarray]):
        return self.Vpps0 * np.exp(-((d - self.d0) / self.delta0))


def main():
    a = SKPotential(1, 1, 1, 1, 1)
    d_list = np.linspace(1, 5, 200)
    vppi = a.Vppi(d_list)
    fig, ax_line = plt.subplots()
    ax_line.plot(d_list, vppi)
    ax_line.set_aspect("auto")
    ax_line.set_xlabel("", fontsize=12)
    ax_line.set_ylabel("", fontsize=12)
    ax_line.set_title("", fontsize=14)
    ax_line.set_xlim(ax_line.get_xlim())
    ax_line.set_ylim(ax_line.get_ylim())
    ax_line.legend([])
    fig.savefig(
        "skp_test.png",
        dpi=330,
        facecolor="w",
        bbox_inches="tight",
        pad_inches=0.1,
    )
    plt.close()
    return


if __name__ == "__main__":
    main()
