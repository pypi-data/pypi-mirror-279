import math


def base_translate(num, base_num):
    """
    将一个十进制数num转换为base_num进制数
    base_translate(21,2)
    [1, 0, 1, 0, 1]
    """
    if num < base_num:
        return [num]
    else:
        n = int(math.log10(num) / math.log10(base_num)) + 1
        output_list = []
        for i in range(n):
            num_add = num // (base_num ** (n - i - 1))
            output_list.append(num_add)
            num = num - num_add * (base_num ** (n - i - 1))
        return output_list


def float_equal(a, b, precision=2):
    """
    判断两个浮点数是否相等
    :param a: value a
    :param b: value b
    :param precision: precision of the comparison
    :return: True or False
    """
    return round(a, precision) == round(b, precision)
