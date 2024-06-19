import multiprocessing
import time


class MultiCal:
    def __init__(
        self, func, x_list: list, other_args_list: list, core=3, disable_hint=True
    ) -> None:
        self.func = func
        self.x_list = x_list
        self.args = other_args_list
        self.core_num = core

        self.disable_hint = disable_hint
        pass

    def _split_xlists(self):
        out_divided_lists = []
        ldivide = len(self.x_list) // self.core_num
        last_i = 0
        for i in range(self.core_num - 1):
            tmp_list = self.x_list[i * ldivide : (i + 1) * ldivide]
            out_divided_lists.append(tmp_list)
            last_i = i
        out_divided_lists.append(self.x_list[(last_i + 1) * ldivide :])
        return out_divided_lists

    def _overdrive_func(
        self,
        core_i,
        list_to_cal,
        trans_out_list,
    ):
        if self.disable_hint:
            ele_list = [self.func(ele, *self.args) for ele in list_to_cal]
        else:
            ele_list = []
            t1 = time.perf_counter()
            for i in range(len(list_to_cal)):
                ele = list_to_cal[i]
                ele_list.append(self.func(ele, *self.args))

                if (i + 1) % (len(list_to_cal) // 10) == 0 and i != 0:
                    t2 = time.perf_counter()
                    print(
                        "{} % are finished, taking {:.3f} min.".format(
                            (i + 1) // (len(list_to_cal) // 10) * 10, (t2 - t1) / 60
                        )
                    )
        ele_list.append(core_i)
        trans_out_list.append(ele_list)

    def calculate(self):
        out_list = multiprocessing.Manager().list()
        p_f = multiprocessing.Pool(self.core_num)

        divided_list = self._split_xlists()
        for i in range(self.core_num):
            p_f.apply_async(
                self._overdrive_func,
                args=(i, divided_list[i], out_list),
            )

        print("Waiting for all subprocesses done...")
        print("Total processes: ", self.core_num)
        p_f.close()
        p_f.join()
        print("All subprocesses done.")

        total_list = []
        for path_i in range(self.core_num):
            for ele_list in out_list:
                if ele_list[-1] == path_i:
                    total_list.extend(ele_list[0:-1])
        return total_list
