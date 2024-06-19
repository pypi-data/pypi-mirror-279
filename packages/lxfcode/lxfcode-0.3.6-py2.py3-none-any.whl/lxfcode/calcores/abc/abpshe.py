# from calcores.filesop.filesave import os, np
import os
import numpy as np
from typing import Literal, Union

# from calcores.pubmeth.pubmeth import ExcelMethod, FilesSave, Line
from ..pubmeth.pubmeth import ExcelMethod, FilesSave, Line
from abc import abstractproperty
from scipy import interpolate
from functools import cached_property
from colorama import Back, Fore, Style


class ExpIFShiftEle:
    def __init__(self, wls, lshift, rshift) -> None:
        self.wls = np.array(wls)
        self.lcp_shift = np.array(lshift)
        self.rcp_shift = np.array(rshift)

    @property
    def lcp_center_y(self):
        return Line(self.wls, self.lcp_shift).center_of_curve()[1]

    @property
    def rcp_center_y(self):
        return Line(self.wls, self.rcp_shift).center_of_curve()[1]

    @property
    def lcp_kb(self):
        return Line(self.wls, self.lcp_shift).kb_of_curve()

    @property
    def rcp_kb(self):
        return Line(self.wls, self.rcp_shift).kb_of_curve()

    @property
    def rcp_lcp_diff_shift(self):
        return self.rcp_shift - self.lcp_shift

    @property
    def lcp_diff(self):
        diff_lcp = np.diff(self.lcp_shift) / np.diff(self.wls)
        return diff_lcp

    @property
    def rcp_diff(self):
        diff_rcp = np.diff(self.rcp_shift) / np.diff(self.wls)
        return diff_rcp


class ExpGHShiftEle:
    def __init__(self, wls, sshift, pshift) -> None:
        self.wls = np.array(wls)
        self.s_shift = sshift
        self.p_shift = pshift

    @property
    def s_center_y(self):
        return Line(self.wls, self.s_shift).center_of_curve()[1]

    @property
    def p_center_y(self):
        return Line(self.wls, self.p_shift).center_of_curve()[1]

    @property
    def s_kb(self):
        return Line(self.wls, self.s_shift).kb_of_curve()

    @property
    def p_kb(self):
        return Line(self.wls, self.p_shift).kb_of_curve()


class SubstrateObj:
    def __init__(self, wls, n) -> None:
        self.wls = wls
        self.n = n

    @cached_property
    def nfunc(self, kind: Literal["linear", "cubic", "quadratic", "zero"] = "linear"):
        f = interpolate.interp1d(self.wls, self.n, kind=kind)
        return f


class ExpDat:
    dataFInst = FilesSave("PSHE/ExpData")

    def __init__(self, if_dat_name="IF_colle", gh_dat_name="GH_colle") -> None:
        self.if_dat_name = if_dat_name + ".xlsx"
        self.gh_dat_name = gh_dat_name + ".xlsx"
        self.exist_if_data = os.path.exists(
            self.dataFInst.target_dir + self.if_dat_name
        )
        self.exist_gh_data = os.path.exists(
            self.dataFInst.target_dir + self.gh_dat_name
        )
        if (not self.exist_if_data) and (not self.exist_gh_data):
            raise FileNotFoundError(
                'Should put the experimental data in the "ExpData" Directory and put the right name in the init function of the class.'
            )

        self._load()

    def _load(self):
        if self.exist_if_data:
            data = ExcelMethod(
                self.dataFInst.target_dir + self.if_dat_name
            ).read_xlsx_data()
            self.iflen = len(data)
            self.if_shifts_list: list[ExpIFShiftEle] = [
                ExpIFShiftEle(*ele_data) for ele_data in data
            ]
        if self.exist_gh_data:
            data = ExcelMethod(
                self.dataFInst.target_dir + self.gh_dat_name
            ).read_xlsx_data()
            self.ghlen = len(data)
            self.gh_shifts_list: list[ExpGHShiftEle] = [
                ExpGHShiftEle(*ele_data) for ele_data in data
            ]

    def plot_gh_data(self):
        if not self.exist_gh_data:
            raise FileNotFoundError("GH data not found")
        scenter_mean = np.mean([ele_if.s_center_y for ele_if in self.gh_shifts_list])
        pcenter_mean = np.mean([ele_if.p_center_y for ele_if in self.gh_shifts_list])

        s_lines = [
            ele_gh.s_shift - ele_gh.s_center_y + scenter_mean
            for ele_gh in self.gh_shifts_list
        ]
        s_wls = [ele_gh.wls for ele_gh in self.gh_shifts_list]
        p_lines = [
            ele_if.p_shift - ele_if.p_center_y + pcenter_mean
            for ele_if in self.gh_shifts_list
        ]
        p_wls = [ele_gh.wls for ele_gh in self.gh_shifts_list]

        Line(s_wls, s_lines, self.dataFInst).multiplot(
            "sshift",
            legends=["Sample {}".format(i + 1) for i in range(self.iflen)],
            xlabel="$\lambda$ (nm)",
            ylabel="$\Delta_{GH}^{s}$",
        )

        Line(p_wls, p_lines, self.dataFInst).multiplot(
            "pshift",
            legends=["Sample {}".format(i + 1) for i in range(self.iflen)],
            xlabel="$\lambda$ (nm)",
            ylabel="$\Delta_{GH}^{p}$",
        )

    def plot_if_data(self):
        if not self.exist_if_data:
            raise FileNotFoundError("IF data not found")
        lcenter_mean = np.mean([ele_gh.lcp_center_y for ele_gh in self.if_shifts_list])
        rcenter_mean = np.mean([ele_gh.rcp_center_y for ele_gh in self.if_shifts_list])

        r_lines = [
            ele_if.rcp_shift - ele_if.rcp_center_y + rcenter_mean
            for ele_if in self.if_shifts_list
        ]
        r_wls = [ele_if.wls for ele_if in self.if_shifts_list]
        l_lines = [
            ele_if.lcp_shift - ele_if.lcp_center_y + lcenter_mean
            for ele_if in self.if_shifts_list
        ]
        l_wls = [ele_if.wls for ele_if in self.if_shifts_list]

        Line(r_wls, r_lines, self.dataFInst).multiplot(
            "rshift",
            legends=["Sample {}".format(i + 1) for i in range(self.iflen)],
            xlabel="$\lambda$ (nm)",
            ylabel="$\Delta_{IF}^{rcp}$",
        )

        Line(l_wls, l_lines, self.dataFInst).multiplot(
            "lshift",
            legends=["Sample {}".format(i + 1) for i in range(self.iflen)],
            xlabel="$\lambda$ (nm)",
            ylabel="$\Delta_{IF}^{lcp}$",
        )

    def plot_diff_if(self):
        if not self.exist_if_data:
            raise FileNotFoundError("IF data not found")
        return


class SubDat:
    dataFInst = FilesSave("PSHE/SubN")

    _instance = None
    _init_flag = False

    def __init__(self, sub_name="SubN") -> None:
        if self._init_flag:
            return
        else:
            self.subN_name = sub_name + ".xlsx"
            data = ExcelMethod(
                self.dataFInst.target_dir + self.subN_name
            ).read_xlsx_data()
            self.sub_list: list[SubstrateObj] = [
                SubstrateObj(*ele_data) for ele_data in data
            ]
            self.sub_len = len(self.sub_list)

            for i in range(len(self.sub_list)):
                print(
                    Fore.GREEN + " Wavelength range for substrate {}: ".format(i),
                    "  ",
                    self.sub_list[i].wls[0],
                    " to ",
                    self.sub_list[i].wls[-1],
                    " nm",
                )
            print(Style.RESET_ALL)
            self._init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
            return cls._instance
        else:
            return cls._instance


class OutDat:
    dataFInst = FilesSave("PSHE/OutN")

    _instance = None
    _init_flag = False

    def __init__(self, out_name="OutN") -> None:
        if self._init_flag:
            return
        else:
            self.outN_name = out_name + ".xlsx"
            data = ExcelMethod(
                self.dataFInst.target_dir + self.outN_name
            ).read_xlsx_data()
            self.out_list: list[SubstrateObj] = [
                SubstrateObj(*ele_data) for ele_data in data
            ]
            self.sub_len = len(self.out_list)
            for i in range(len(self.out_list)):
                print(
                    Fore.GREEN + " Wavelength range for out medium {}: ".format(i),
                    "  ",
                    self.out_list[i].wls[0],
                    " to ",
                    self.out_list[i].wls[-1],
                    " nm",
                )
            print(Style.RESET_ALL)
            self._init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
            return cls._instance
        else:
            return cls._instance


def main():
    ExpDat()
    np.ndarray
    return


if __name__ == "__main__":
    main()
