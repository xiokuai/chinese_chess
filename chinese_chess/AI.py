"""
电脑算法
"""

import ctypes
import alpha_beta_search
import min_max_search
from configure import config

_cpp_lib = ctypes.WinDLL('./alpha_beta_search.dll')

# 设置 search 函数签名
_cpp_lib.search.argtypes = [
    ctypes.POINTER((ctypes.c_int * 9) * 10),  # board: 10x9 数组
    ctypes.c_int,                             # depth
    ctypes.POINTER(ctypes.c_int * 4),         # result: 4个int的数组
    ctypes.c_bool                             # reverse
]
_cpp_lib.search.restype = ctypes.c_float

id: dict[str, int] = {
    '将': -1,
    '士': -2,
    '象': -3,
    '卒': -4,
    '马': -6,
    '炮': -7,
    '车': -8,
    '帥': 1,
    '仕': 2,
    '相': 3,
    '兵': 4,
    '馬': 6,
    '砲': 7,
    '車': 8,
}


def _lst_to_array(data: list[list[int]]) -> ctypes.Array[ctypes.Array[ctypes.c_int]]:
    """Python 二维棋局列表转换为 C 二维数组"""
    arr = (ctypes.c_int * 9 * 10)()
    for i in range(10):
        for j in range(9):
            arr[i][j] = data[i][j]
    return arr


def choose_algo(data: list[list[int]], depth: int, reverse: bool) -> alpha_beta_search.Node:
    """"""
    match config["algo"]:
        case 1:
            # 极小极大搜索算法
            node = min_max_search.min_max_search(data, depth, reverse=reverse)
        case 2:
            # α-β 剪枝算法
            node = alpha_beta_search.alpha_beta_search(data, depth, reverse=reverse)
        case _:
            # α-β 剪枝算法（C++ 实现）
            result = (ctypes.c_int * 4)()
            c_data = _lst_to_array(data)
            score = _cpp_lib.search(c_data, depth, result, reverse)
            operation = ((result[0], result[1]), (result[2], result[3]))
            return alpha_beta_search.Node(score, operation)

    if node.operation[0][0] == -1:
        node.operation = None
    return node


def intelligence(chesses: list[list], color: str, depth: int) -> tuple[tuple[tuple[int, int], tuple[bool, int, int]] | None, int]:
    """"""
    data = [[0]*9 for _ in range(10)]
    for i, line in enumerate(chesses):
        for j, chess in enumerate(line):
            if chess is not None:
                data[i][j] = id[chess.name]
                if data[i][j] == -4 and i >= 5:  # 卒兵过河类型转变
                    data[i][j] = -5
                elif data[i][j] == 4 and i <= 4:
                    data[i][j] = 5

    node = choose_algo(data, depth, color != "#FF0000")

    if node.operation is None:
        return None, node.score
    (ci, cj), (ti, tj) = node.operation
    flag = data[ti][tj] != 0
    ti -= ci
    tj -= cj
    return ((cj, ci), (flag, tj, ti)), node.score
