"""
工具函数
"""

from game import game
from constants import FEN
from tkinter import filedialog
import rule


def print_chess(chesses: list[list], step: list[int] = [0]) -> None:
    """输出当前棋局"""
    step[0] += 1
    print("\033[36mSTEP\033[0m:", step[0])
    for line in chesses:
        for chess in line:
            if chess is None:
                print("〇", end="")
            elif chess.name in "将士象马车炮卒":
                print(f"\033[32m{chess.name}\033[0m", end="")
            else:
                print(f"\033[31m{chess.name}\033[0m", end="")
        print()
    print()


def clear() -> None:
    """清空棋盘"""
    for y, line in enumerate(game.chesses):
        for x, chess in enumerate(line):
            if chess:
                chess.destroy()
                game.chesses[y][x] = None


def open_file(path: str | None = None) -> None:
    """打开文件"""
    from chess import Chess
    from GUI import Window

    if path or (
        path := filedialog.askopenfilename(
            title="导入棋局", filetypes=[("象棋文件", "*.fen")]
        )
    ):
        try:
            with open(path, "r", encoding="utf-8") as file:
                code, first = file.read().split()
            fen = {value: key for key, value in FEN.items()}
            clear()
            for y, line in enumerate(code.split("/")):
                x = 0
                for i in line:
                    if i.isalpha():
                        color = "#FF0000" if i.isupper() else "#000000"
                        Chess(fen[i], x, y, color)
                    x += int(i) if i.isdigit() else 1
            game.first = first != "b"
            rule.modechange("END")
        except:
            Window.tip("— 提示 —\n象棋文件格式不正确！\n导入棋局失败！")


def save_file(code: str = "") -> None:
    """另存为文件"""
    if path := filedialog.asksaveasfilename(
        title="导出棋局", filetypes=[("象棋文件", "*.fen")], initialfile="Chess.fen"
    ):
        for line in game.chesses:
            code, count = code + "/", 0
            for chess in line:
                if chess:
                    code += str(count) + FEN[chess.name]
                    count = 0
                else:
                    count += 1
            code += str(count)
        first = "r" if game.first else "b"
        with open(path, "w", encoding="utf-8") as file:
            file.write("%s %s" % (code.replace("0", "")[1:], first))
