"""
所有常量
"""

from socket import gethostbyname, gethostname
from tkinter import Tk

import tkintertools as tkt
from configure import config, configure
from l10n import _

# 当前地址
ADDRESS = gethostbyname(gethostname())
# 默认端口
PORT = 10086
# 服务器地址
SERVER_ADDRESS = ""

# 红方虚拟棋子文本颜色
VIRTUAL_RED = "#D05C2D"
# 黑方虚拟棋子文本颜色
VIRTUAL_BLACK = "#845C2D"
# 虚拟棋子外框颜色
VIRTUAL_OUTLINE = "#845C2D"
# 虚拟棋子外框颜色
VIRTUAL_INSIDE = "#A06F36"
# 棋盘背景颜色
BACKGROUND = "#BC8340"

# 棋子分值
EXIST_DICT = {
    "将": 1000,
    "士": 4,
    "象": 4,
    "马": 8,
    "车": 18,
    "炮": 9,
    "卒": 3,
    "帥": 1000,
    "仕": 4,
    "相": 4,
    "馬": 8,
    "車": 18,
    "砲": 9,
    "兵": 3,
}

# FEN棋谱规定
FEN = {
    "将": "k",
    "士": "a",
    "象": "b",
    "马": "n",
    "车": "r",
    "炮": "c",
    "卒": "p",
    "帥": "K",
    "仕": "A",
    "相": "B",
    "馬": "N",
    "車": "R",
    "砲": "C",
    "兵": "P",
}

# 统计数据名称对照表
STATISTIC_DICT = {
    "Launch": _("程序启动次数"),
    "LAN": _("联机模式使用次数"),
    "LOCAL": _("双人模式使用次数"),
    "COMPUTER": _("人机模式使用次数"),
    "END": _("残局模式使用次数"),
    "TEST": _("测试模式使用次数"),
    "Revoke": _("悔棋次数"),
    "Recovery": _("撤销悔棋次数"),
    "AI": _("AI功能调用次数"),
    "Eat": _("吃棋次数"),
    "Move": _("移棋次数"),
    "Warn": _("“将军”次数"),
    "Win": _("游戏胜利次数"),
    "Lose": _("游戏失败次数"),
    "Peace": _("和棋次数"),
    "Play": _("对局次数"),
    "Time": _("总游戏时间"),
    "First": _("先手次数"),
}

# 选子音效
VOICE_CHOOSE = "audio/choose.wav"
# 落子音效
VOICE_DROP = "audio/drop.wav"
# 吃子音效
VOICE_EAT = "audio/eat.wav"
# “将军”音效
VOICE_WARN = "audio/warn.wav"
# 按钮音效
VOICE_BUTTON = "audio/button.wav"

_TK = Tk()
_TK.withdraw()

# 屏幕宽度
SCREEN_WIDTH = _TK.winfo_screenwidth()
# 屏幕高度
SCREEN_HEIGHT = _TK.winfo_screenheight() - 40

# 窗口缩放系数
if config["auto_scale"]:
    S = format(SCREEN_HEIGHT / tkt.S / (710 + 50), ".3f")
    S = float(S)
    configure(scale=S)
else:
    S = config["scale"]
