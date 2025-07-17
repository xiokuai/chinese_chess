import rule
from math import hypot
from chinese_chess_lib import dead, warn, Chess as CChess
import LAN
import tkintertools as tkt
from winsound import SND_ASYNC, PlaySound
from constants import VOICE_EAT, VOICE_DROP, VOICE_WARN, VOICE_CHOOSE, VIRTUAL_OUTLINE, VIRTUAL_INSIDE, VIRTUAL_RED, VIRTUAL_BLACK
from constants import S
from configure import statistic
from tools import print_chess
from tkinter import Event

class Chess:
    """ 棋子 """

    def __init__(self, name: str, x: int, y: int, color: bool) -> None:
        """ 初始化 """
        # 延迟导入，避免循环依赖
        from GUI import Window, game
        self.name = name  # 名称，区分类别
        self.color = color  # 颜色，区分红黑
        self.x, self.y = x, y
        game.chesses[y][x] = self
        x, y = 40+x*70, 40+y*70
        self.items = [
            Window.canvas.create_oval(  # 阴影
                (x-28)*S, (y-28)*S, (x+32)*S, (y+32)*S, fill='#505050', width=0),
            Window.canvas.create_oval(  # 外框
                (x-30)*S, (y-30)*S, (x+30)*S, (y+30)*S, fill='#B49632'),
            Window.canvas.create_oval(  # 内框
                (x-27)*S, (y-27)*S, (x+27)*S, (y+27)*S, fill='#D2B450', width=0),
            Window.canvas.create_text(  # 文字
                x*S, y*S, text=name, font=('楷体', round(27*S), 'bold'), fill=color)
        ]  # type: list[int]
        self.virtual_items = []  # type: list[int]
        self.attack_chess = []  # type: list[Chess]
        self.move_pos: list[tuple[int, int]] = []

    def lift(self) -> None:
        from GUI import Window
        Window.canvas.lift(self.items[0])
        Window.canvas.lift(self.items[1])
        Window.canvas.lift(self.items[2])
        Window.canvas.lift(self.items[3])

    def move(self, flag: bool, x: int, y: int, cache: bool = False) -> None:
        from GUI import Window, game, convert_to_CChesses
        statistic(Move=1)
        self.lift()
        self.virtual_delete()
        self.x += x
        self.y += y

        if not cache:
            game.chesses[self.y-y][self.x-x] = None
            game.index += 1
            if game.index == len(game.cache):  # 新增
                game.cache.append(  # (目标者名称，目标位置，回退位移)
                    (getattr(game.chesses[self.y][self.x], 'name', None), (self.x, self.y), (-x, -y)))
            else:  # 覆盖
                game.cache[game.index] = (
                    (getattr(game.chesses[self.y][self.x], 'name', None), (self.x, self.y), (-x, -y)))

        def update() -> None:
            """ 更新并播放音效 """
            from GUI import game, convert_to_CChesses
            if flag:
                statistic(Eat=1)
                game.count = 0
                game.chesses[self.y][self.x].destroy()
            else:
                game.count += 1
            game.chesses[self.y][self.x] = self
            if rule.peace():  # 和棋
                rule.gameover()
                if game.mode == 'LAN':
                    LAN.API.close()
            elif not (color := warn(convert_to_CChesses(game.chesses), self.color)):
                file = VOICE_EAT if flag else VOICE_DROP
                PlaySound(file, SND_ASYNC)
            else:
                PlaySound(VOICE_WARN, SND_ASYNC)
                statistic(Warn=1)
                if dead(convert_to_CChesses(game.chesses), color[0]):  # 绝杀
                    rule.gameover(color[0])
                    if game.mode == 'LAN':
                        LAN.API.close()

            print_chess(game.chesses)

        for item in self.items:
            tkt.move(Window.canvas, item, x*70*S, y*70*S, 500, 'smooth',
                     end=update if not self.items.index(item) else None)

    def destroy(self) -> None:
        from GUI import Window
        Window.canvas.delete(*self.items)
        self.virtual_delete()

    def highlight(self, condition: bool, color: str | None = None, inside: bool = True) -> bool:
        from GUI import Window
        if condition:
            if not inside:
                PlaySound(VOICE_CHOOSE, SND_ASYNC)
            Window.canvas.itemconfigure(self.items[1+inside], fill=color)
        else:
            color_ = '#D2B450' if inside else '#B49632'
            Window.canvas.itemconfigure(self.items[1+inside], fill=color_)
        return condition

    def touch(self, event: Event) -> bool:
        import tkintertools as tkt
        """ 触碰棋子 """
        x, y = (40+self.x*70)*S, (40+self.y*70)*S
        condition = hypot(event.x/tkt.S-x, event.y/tkt.S-y) < 30*S
        return self.highlight(condition, '#E4D296')

    def choose(self, event: Event) -> bool:
        import tkintertools as tkt
        """ 选中棋子 """
        x, y = (40+self.x*70)*S, (40+self.y*70)*S
        condition = hypot(event.x/tkt.S-x, event.y/tkt.S-y) < 30*S
        if not self.highlight(condition, '#00FF00', False):
            self.virtual_delete()
        return condition

    def virtual(self, flag: bool, x: int, y: int) -> None:
        from GUI import Window, game
        """ 虚位显示 """
        if flag:
            chess = game.chesses[self.y+y][self.x+x]
            self.attack_chess.append(chess)
            chess.highlight(True, '#FF0000', False)
        else:
            x, y = 40+(self.x+x)*70, 40+(self.y+y)*70
            self.virtual_items.append(Window.canvas.create_oval(  # 外框
                (x-30)*S, (y-30)*S, (x+30)*S, (y+30)*S, fill='', outline=VIRTUAL_OUTLINE))
            self.virtual_items.append(Window.canvas.create_oval(  # 内框
                (x-27)*S, (y-27)*S, (x+27)*S, (y+27)*S, fill='', outline=VIRTUAL_INSIDE))
            self.virtual_items.append(Window.canvas.create_text(  # 文字
                x*S, y*S, text=self.name, font=('楷体', int(27*S), 'bold'),
                fill=VIRTUAL_RED if self.color == '#FF0000' else VIRTUAL_BLACK))

    def virtual_delete(self) -> None:
        from GUI import Window
        """ 删除虚位显示 """
        for chess in self.attack_chess:
            chess.highlight(False, inside=False)
        self.attack_chess.clear()
        Window.canvas.delete(*self.virtual_items)

def convert_to_CChesses(chesses):
    """将GUI棋盘转换为CChess棋盘"""
    cchess_board = []
    for y, row in enumerate(chesses):
        c_row = []
        for x, chess in enumerate(row):
            if chess:
                c = CChess()
                c.x = chess.x
                c.y = chess.y
                c.color = chess.color
                c.name = chess.name
                c_row.append(c)
            else:
                c_row.append(None)
        cchess_board.append(c_row)
    return cchess_board

def convert_to_CChess(chess):
    """将GUI棋子转换为CChess棋子"""
    if chess is None:
        return None
    c = CChess()
    c.x = chess.x
    c.y = chess.y
    c.color = chess.color
    c.name = chess.name
    return c
