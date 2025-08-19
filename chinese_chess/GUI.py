"""
图形界面
"""

from math import hypot
import os
from sys import exit
from threading import Thread
from time import time
from tkinter import Event, IntVar, Menu, ttk
from chess import Chess, convert_to_CChesses, convert_to_CChess
from game import game
from mini_win import MiniWin, HelpWin, StatisticWin, LibraryWin, SettingWin, AboutWin
from chinese_chess_lib import get_legal_moves
from l10n import _

import LAN
import rule
import tkintertools as tkt
from AI import intelligence
from configure import config, statistic
from constants import BACKGROUND, SCREEN_WIDTH, VOICE_BUTTON, S
from main import __author__, __update__, __version__
from tools import open_file, save_file, clear
from sound import play_sound_async


class Window:
    """主窗口"""

    root = tkt.Tk(
        "Chinese Chess by李悟/梁晨轩",
        int(640 * S),
        int(710 * S),
        (SCREEN_WIDTH - tkt.S * 640 * S) // 2,
        0,
        exit,
        os.path.abspath("logo.ico"),
    )
    root.resizable(False, False)
    menu = Menu(root, tearoff=False)
    root.configure(menu=menu)
    canvas = tkt.Canvas(root, 640 * S, 710 * S, bg=BACKGROUND, expand=False)
    canvas.place(x=0, y=0)
    timer = canvas.create_text(
        320 * S,
        355 * S,
        font=("楷体", int(20 * S)),
        justify="center",
        text="00:00\n- 中国象棋 -",
    )

    def __init__(self) -> None:
        """初始化"""
        self.inZenMode = 0
        self.init_menu()
        self.init_bind()
        self.init_board()
        self.new()

        self.root.mainloop()

    def activate_zen_mode(self):
        if self.inZenMode == 1:
            self.root.attributes("-fullscreen", False)  # 退出全屏
            self.root.overrideredirect(False)  # 恢复边框

            # 恢复默认布局
            self.canvas.place(x=0, y=0)
            self.inZenMode = 0
        else:
            self.root.attributes("-fullscreen", True)  # 全屏
            self.root.configure(bg="black")  # 黑色背景
            self.root.overrideredirect(True)  # 隐藏边框
            # 使用相对坐标和锚点居中画布
            self.canvas.place(relx=0.5, rely=0.5, anchor="center")
            self.inZenMode = 1

    def init_menu(self) -> None:
        """菜单栏"""
        m1 = Menu(self.menu, tearoff=False)
        m2 = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label=_("选项(O)"), menu=m1)
        self.menu.add_cascade(label=_("帮助(H)"), menu=m2)
        m1.add_command(label=_("导入棋局"), command=open_file, accelerator="Ctrl+O")
        m1.add_command(label=_("导出棋局"), command=save_file, accelerator="Ctrl+S")
        m1.add_command(label=_("棋局库"), command=lambda: LibraryWin(self.root))
        m1.add_separator()
        m1.add_command(label=_("撤销"), accelerator="Ctrl+Z", command=rule.revoke)
        m1.add_command(label=_("恢复"), accelerator="Ctrl+Y", command=rule.recovery)
        m1.add_separator()
        m1.add_command(label=_("游戏设置"), command=lambda: SettingWin(self.root))
        m1.add_command(label=_("新游戏"), accelerator="Ctrl+N", command=self.new)
        m1.add_command(label=_("退出"), accelerator="Ctrl+Q", command=exit)
        m2.add_command(
            label=_("游戏说明"),
            accelerator="Ctrl+H",
            command=lambda: HelpWin(self.root),
        )
        m2.add_command(label=_("统计数据"), command=lambda: StatisticWin(self.root))
        m2.add_separator()
        m2.add_command(label=_("关于"), command=lambda: AboutWin(self.root))

    def init_bind(self) -> None:
        """绑定"""
        self.root.bind("<Motion>", self.touch)
        self.root.bind("<Button-1>", self.choose)
        self.root.bind("<Control-h>", lambda _: HelpWin(self.root))  # 游戏说明
        self.root.bind("<Control-z>", lambda _: rule.revoke())  # 撤销
        self.root.bind("<Control-y>", lambda _: rule.recovery())  # 恢复
        self.root.bind("<Control-o>", lambda _: open_file())  # 打开
        self.root.bind("<Control-s>", lambda _: save_file())  # 另存为…
        self.root.bind("<Control-n>", lambda _: self.new())  # 新游戏
        self.root.bind("<Control-q>", lambda _: self.root.quit())  # 退出
        self.root.bind("<Control-t>", lambda _: self.test())  # AI测试
        self.root.bind("<z>", lambda _: self.activate_zen_mode())  # 进/出禅意模式

    def init_board(self) -> None:
        """棋盘"""

        def point(x: int, y: int) -> None:
            """关键点"""
            a, b = 5 * S, 25 * S  # 间距，长度
            if x != 40 * S:
                self.canvas.create_line(x - b, y - a, x - a, y - a, x - a, y - b)
                self.canvas.create_line(x - a, y + b, x - a, y + a, x - b, y + a)
            if x != 600 * S:
                self.canvas.create_line(x + a, y - b, x + a, y - a, x + b, y - a)
                self.canvas.create_line(x + b, y + a, x + a, y + a, x + a, y + b)

        self.canvas.create_text(
            320 * S,
            355 * S,
            text="楚 河" + "\t" * 2 + "汉 界",
            font=("华文行楷", int(40 * S)),
        )

        self.canvas.create_rectangle(32 * S, 32 * S, 608 * S, 678 * S, width=3)
        self.canvas.create_rectangle(40 * S, 40 * S, 600 * S, 670 * S)
        self.canvas.create_line(250 * S, 40 * S, 390 * S, 180 * S)
        self.canvas.create_line(250 * S, 530 * S, 390 * S, 670 * S)
        self.canvas.create_line(390 * S, 40 * S, 250 * S, 180 * S)
        self.canvas.create_line(390 * S, 530 * S, 250 * S, 670 * S)

        point(110 * S, 180 * S)
        point(530 * S, 180 * S)
        point(110 * S, 530 * S)
        point(530 * S, 530 * S)

        for x in 40, 180, 320, 460, 600:
            point(x * S, 250 * S)
            point(x * S, 460 * S)

        for x in range(7):
            _ = 110 + x * 70
            self.canvas.create_line(_ * S, 40 * S, _ * S, 320 * S)
            self.canvas.create_line(_ * S, 390 * S, _ * S, 670 * S)
        for y in range(8):
            _ = 110 + y * 70
            self.canvas.create_line(40 * S, _ * S, 600 * S, _ * S)

    def new(self) -> None:
        """新游戏页面"""
        m = MiniWin(self.root, _("选择模式"), 300, 150)
        toplevel, canvas = m.toplevel, m.canvas
        canvas.configure(bg="#FFFFFF")
        toplevel.var_list = [IntVar(toplevel, not i) for i in range(13)]

        def canvas_set(mode: str) -> None:
            """设定次级画布"""
            canvas_ = tkt.Canvas(toplevel, 300 * S, 150 * S, expand=False)
            canvas_.place(x=0, y=0)

            last = tkt.CanvasButton(
                canvas_,
                6 * S,
                121 * S,
                80 * S,
                23 * S,
                6 * S,
                font=("楷体", round(12 * S)),
                text=_("上一步"),
                command=lambda: (toplevel.title(_("选择模式")), canvas_.destroy()),
            )
            last.command_ex["press"] = lambda: play_sound_async(VOICE_BUTTON)

            if mode in "COMPUTER LOCAL":
                more_set(toplevel, canvas_)
                last.move(122 * S, 0)
                tkt.CanvasButton(
                    canvas_,
                    214 * S,
                    121 * S,
                    80 * S,
                    23 * S,
                    6 * S,
                    font=("楷体", round(12 * S)),
                    text=_("开始"),
                    command=lambda: (
                        rule.modechange(
                            mode, "".join([str(v.get()) for v in toplevel.var_list])
                        ),
                        toplevel.destroy(),
                    ),
                ).command_ex["press"] = lambda: play_sound_async(VOICE_BUTTON)
                toplevel.title(
                    _("选择模式 - ")
                    + (_("双人对弈") if mode == "LOCAL" else _("人机对战"))
                )
            elif mode == "LAN":
                toplevel.title(_("选择模式 - 联机对抗"))
                info = canvas_.create_text(
                    150 * S,
                    85 * S,
                    font=("楷体", round(10 * S)),
                    justify="center",
                    text=_("请选择连接方式"),
                )
                tkt.CanvasButton(
                    canvas_,
                    20 * S,
                    20 * S,
                    120 * S,
                    30 * S,
                    8 * S,
                    _("客户端连接"),
                    font=("楷体", round(12 * S)),
                    command=lambda: (
                        LAN.API.init(toplevel, "CLIENT"),
                        play_sound_async(VOICE_BUTTON),
                    ),
                ).command_ex["touch"] = lambda: canvas_.itemconfigure(
                    info,
                    text=_("主动的连接方式\n套接字将主动搜索局域网内可识别的服务端"),
                )
                tkt.CanvasButton(
                    canvas_,
                    160 * S,
                    20 * S,
                    120 * S,
                    30 * S,
                    8 * S,
                    _("服务端连接"),
                    font=("楷体", round(12 * S)),
                    command=lambda: (
                        LAN.API.init(toplevel, "SERVER"),
                        play_sound_async(VOICE_BUTTON),
                    ),
                ).command_ex["touch"] = lambda: canvas_.itemconfigure(
                    info, text=_("被动的连接方式\n套接字将惰性地等待可能的客户端的连接")
                )

        tkt.CanvasButton(
            canvas,
            25 * S,
            15 * S,
            70 * S,
            70 * S,
            10 * S,
            "AI",
            font=("方正舒体", round(50 * S), "bold"),
            command=lambda: (canvas_set("COMPUTER"), play_sound_async(VOICE_BUTTON)),
        ).command_ex["touch"] = lambda: canvas.itemconfigure(
            text, text=_("人脑与电脑的激烈碰撞！")
        )
        tkt.CanvasButton(
            canvas,
            115 * S,
            15 * S,
            70 * S,
            70 * S,
            10 * S,
            "将",
            font=("方正舒体", round(50 * S), "bold"),
            command=lambda: (canvas_set("LOCAL"), play_sound_async(VOICE_BUTTON)),
        ).command_ex["touch"] = lambda: canvas.itemconfigure(
            text, text=_("双方激烈对峙，到底谁能笑到最后？")
        )
        tkt.CanvasButton(
            canvas,
            205 * S,
            15 * S,
            70 * S,
            70 * S,
            10 * S,
            "帥",
            font=("方正舒体", round(50 * S), "bold"),
            command=lambda: (canvas_set("LAN"), play_sound_async(VOICE_BUTTON)),
        ).command_ex["touch"] = lambda: canvas.itemconfigure(
            text, text=_("和局域网里的朋友一起玩耍吧！")
        )
        canvas.create_text(
            60 * S, 100 * S, text=_("人机对战"), font=("楷体", round(12 * S))
        )
        canvas.create_text(
            150 * S, 100 * S, text=_("双人对弈"), font=("楷体", round(12 * S))
        )
        canvas.create_text(
            240 * S, 100 * S, text=_("联机对抗"), font=("楷体", round(12 * S))
        )
        canvas.create_rectangle(-1, 115 * S, 301 * S, 151 * S, width=0, fill="#F1F1F1")
        text = canvas.create_text(
            150 * S, 132 * S, text=_("请选择游戏模式"), font=("楷体", round(12 * S))
        )

    @classmethod
    def chess(cls) -> None:
        """初始化棋子"""
        clear()
        for i in 1, 7:
            Chess("炮", i, 2, "#000000")
            Chess("砲", i, 7, "#FF0000")
        for x in range(0, 10, 2):
            Chess("兵", x, 6, "#FF0000")
            Chess("卒", x, 3, "#000000")
        for a, b, i in zip("车马象士将士象马车", "車馬相仕帥仕相馬車", range(9)):
            Chess(a, i, 0, "#000000")
            Chess(b, i, 9, "#FF0000")

    @classmethod
    def clock(cls, flag: list[int | None] = [0, None]) -> None:
        """计时"""
        if (flag[1] and flag[1] != game.timer) or not game.player:
            return statistic(Time=flag[0])
        if not flag[1]:
            game.timer = flag[1] = time()
        cls.canvas.itemconfigure(
            cls.timer,
            text=_("%02d:%02d\n%s思考中.") % (*divmod(flag[0], 60), game.player)
            + "." * (flag[0] % 3),
        )
        cls.root.after(1000, cls.clock, [flag[0] + 1, flag[1]])

    @classmethod
    def touch(cls, event: Event) -> None:
        """高亮选棋"""
        flag = True
        for line in game.chesses:
            for chess in line:
                if chess:
                    if chess.touch(event) and flag:
                        flag = False
                        cls.canvas.configure(cursor="hand2")
        if flag:
            cls.canvas.configure(cursor="arrow")

    @classmethod
    def choose(cls, event: Event, chess_=None) -> None:
        """选中棋子"""
        if not (game.choose and cls.move(game.choose, event)):
            for chess in [chess for line in game.chesses for chess in line]:
                if chess and rule.ifop(chess, game.player):
                    if chess.choose(event):
                        chess_ = chess
        game.choose = chess_
        if chess_:
            cchess_board = convert_to_CChesses(game.chesses)
            cchess_obj = convert_to_CChess(chess_)
            chess_.move_pos = get_legal_moves(cchess_board, cchess_obj, True)
            if config["virtual"]:
                for pos in chess_.move_pos:
                    chess_.virtual(*pos)

    @classmethod
    def move(
        cls,
        choose,  # type: Chess
        event: Event,
    ) -> bool | None:
        """移动棋子"""
        for flag, x_, y_ in choose.move_pos:
            x, y = (40 + (choose.x + x_) * 70) * S, (40 + (choose.y + y_) * 70) * S
            if hypot(event.x / tkt.S - x, event.y / tkt.S - y) < 30 * S:
                if game.mode == "LAN":
                    LAN.API.send(msg=(choose.x, choose.y, flag, x_, y_))
                choose.move(flag, x_, y_)
                choose.highlight(False, inside=False)
                choose = None
                if game.mode in ("COMPUTER", "END"):
                    cls.root.after(
                        700,
                        Thread(
                            target=lambda: Window.AImove("#000000"), daemon=True
                        ).start,
                    )
                rule.switch()
                return True

    @classmethod
    def AImove(cls, color: str, flag: bool = False) -> None:
        """电脑移动"""
        if not game.player:
            return
        # statistic(AI=1)
        data, score = intelligence(game.chesses, color, config["level"])
        if data == None:
            rule.gameover(color[0])
        print("\033[33mSCORE\033[0m:", score)
        pos, delta = data
        game.chesses[pos[1]][pos[0]].move(*delta)
        rule.switch()
        if flag and game.mode == "TEST":
            color = "#FF0000" if color == "#000000" else "#000000"
            cls.root.after(
                600, Thread(target=cls.AImove, args=(color, True), daemon=True).start
            )

    @classmethod
    def tip(cls, text: str, stay: int = 3000) -> None:
        """产生一个提示框"""
        label = tkt.CanvasLabel(
            cls.canvas,
            -250 * S,
            10 * S,
            240 * S,
            120 * S,
            20 * S,
            text,
            font=("楷体", round(15 * S)),
            color_outline=["black", "black"],
        )
        icon = tkt.CanvasLabel(
            cls.canvas,
            -240 * S,
            20 * S,
            30 * S,
            30 * S,
            15 * S,
            " i  ",
            font=("华文隶书", round(20 * S), "bold"),
            color_text=["#4884B4", "#4884B4"],
            color_outline=["grey", "grey"],
            color_fill=tkt.COLOR_NONE,
        )
        tkt.move(cls.canvas, label, 260 * S, 0, 500, "smooth")
        tkt.move(cls.canvas, icon, 260 * S, 0, 500, "smooth")
        cls.root.after(stay, tkt.move, cls.canvas, label, -260 * S, 0, 500, "smooth")
        cls.root.after(stay, tkt.move, cls.canvas, icon, -260 * S, 0, 500, "smooth")
        cls.root.after(stay + 1000, label.destroy)
        cls.root.after(stay + 1000, icon.destroy)

    @classmethod
    def test(cls, color: str = "#FF0000") -> None:
        """测试模式"""
        rule.modechange("TEST")
        cls.root.after(
            4000, Thread(target=cls.AImove, args=(color, True), daemon=True).start
        )


def more_set(toplevel: tkt.Toplevel, canvas: tkt.Canvas | None = None) -> None:
    """更多设置"""
    if not canvas:
        canvas = tkt.Canvas(toplevel, 300 * S, 150 * S, expand=False)
        canvas.place(x=0, y=0)
        tkt.CanvasButton(
            canvas,
            214 * S,
            121 * S,
            80 * S,
            23 * S,
            6 * S,
            _("返回"),
            font=("楷体", round(12 * S)),
            command=canvas.destroy,
        ).command_ex["press"] = lambda: play_sound_async(VOICE_BUTTON)

    ttk.Style(canvas).configure("TCheckbutton", font=("楷体", round(12 * S)))
    canvas.create_text(75 * S, 15 * S, text=_("我方让子"), font=("楷体", round(12 * S)))
    canvas.create_text(
        225 * S, 15 * S, text=_("对方让子"), font=("楷体", round(12 * S))
    )
    ttk.Checkbutton(
        canvas, text=_("我方先手"), variable=toplevel.var_list[0], onvalue=1, offvalue=0
    ).place(
        width=100 * tkt.S * S,
        height=30 * tkt.S * S,
        x=10 * tkt.S * S,
        y=117 * tkt.S * S,
    )

    for y_, y in enumerate([30, 60, 90]):
        for x_, x in enumerate([10, 85, 160, 235]):
            i = y_ * 4 + x_
            text = ("右" if i & 1 else "左") + "車车砲炮馬马"[i // 2]
            ttk.Checkbutton(
                canvas,
                text=text,
                onvalue=1,
                offvalue=0,
                variable=toplevel.var_list[i + 1],
            ).place(
                width=100 * tkt.S * S,
                height=30 * tkt.S * S,
                x=x * tkt.S * S,
                y=y * tkt.S * S,
            )
