"""
游戏规则控制
"""

from threading import Thread

from configure import config, statistic

from l10n import _


def peace() -> bool:
    """和棋判定"""
    import GUI

    if GUI.game.count >= config["peace"] * 2:
        return True
    if (ind := GUI.game.index) >= 11:
        if GUI.game.cache[ind - 3 : ind + 1] * 2 == GUI.game.cache[ind - 11 : ind - 3]:
            return True
    return False


def gameover(color: str | None = None) -> None:
    """游戏结束逻辑处理"""
    import GUI
    from tkinter import messagebox

    # 清除玩家状态
    GUI.game.player = None
    GUI.game.choose = None

    # 和棋情况
    if color is None:
        statistic(Peace=1)
        GUI.Window.root.after(
            0, lambda: messagebox.showinfo("游戏结束", "本局和棋！\t")
        )
        return

    # 判断胜负
    is_red = color == "#FF0000"
    is_local_test = GUI.game.mode in ("LOCAL", "TEST")

    if is_local_test:
        tone = ""
        win = _("获胜!")
        who = _("红方") if is_red else _("黑方")
    else:
        tone = _("恭喜你!") if is_red else _("很遗憾")
        win = _("赢了!") if is_red else _("输了.")
        who = _("你")

    # 统计结果
    if win == _("赢了!"):
        statistic(Win=1)
    elif win == _("输了."):
        statistic(Lose=1)

    # 弹窗提示
    GUI.Window.root.after(0, lambda: messagebox.showinfo(tone, who + win))

    # 重置界面定时器显示
    GUI.Window.canvas.itemconfigure(GUI.Window.timer, text="00:00\n- 中国象棋 -")


def ifop(chess, player: str) -> bool:
    """是否可操作"""
    import GUI

    if not GUI.game.mode or not player:
        return False
    if GUI.game.mode in "COMPUTER END":
        return player == "玩家" and chess.color == "#FF0000"
    elif GUI.game.mode == "LAN" or "SERVER":
        return player == "我方" and chess.color == "#FF0000"
    elif GUI.game.mode == "LOCAL":
        return player[0] == "红黑"[chess.color == "#000000"]
    return False


def switch() -> None:
    """切换走棋方"""
    import GUI

    if GUI.game.player:
        if GUI.game.mode in "COMPUTER END":
            GUI.game.player = "玩家" if GUI.game.player == "电脑" else "电脑"
        elif GUI.game.mode == "LAN" or "SERVER":
            GUI.game.player = "我方" if GUI.game.player == "对方" else "对方"
        else:
            GUI.game.player = "红方" if GUI.game.player == "黑方" else "黑方"
    else:
        if GUI.game.first:
            if GUI.game.mode in "LAN SERVER COMPUTER END":
                statistic(First=1)
            GUI.game.player = (
                "我方"
                if GUI.game.mode == "LAN" or "SERVER"
                else "玩家" if GUI.game.mode in "COMPUTER END" else "红方"
            )
        else:
            GUI.game.player = (
                "对方"
                if GUI.game.mode == "LAN" or "SREVER"
                else "电脑" if GUI.game.mode in "COMPUTER END" else "黑方"
            )
    GUI.Window.clock([0, None])


def gameset(code: str | None = None) -> None:
    """游戏设定"""
    if code:
        import GUI

        GUI.game.first = bool(int(code[0]))
        lis = [
            (0, 9),
            (8, 9),
            (0, 0),
            (8, 0),
            (1, 7),
            (7, 7),
            (1, 2),
            (7, 2),
            (1, 9),
            (7, 9),
            (1, 0),
            (7, 0),
        ]
        for i, v in enumerate(code):
            if int(v) and i:
                x, y = lis[i - 1]
                GUI.game.chesses[y][x].destroy()
                GUI.game.chesses[y][x] = None


def modechange(mode: str, code: str | None = None) -> None:
    """改变模式"""
    import GUI

    if mode != "END":
        GUI.Window.chess()
    GUI.game.cache.clear()
    GUI.game.index = -1
    GUI.game.count = 0
    GUI.game.mode = mode
    GUI.game.choose = None
    gameset(code)
    statistic(**{"Play": 1, mode: 1})
    mode = (
        "双人对弈"
        if mode == "LOCAL"
        else (
            "联机对抗"
            if mode == "LAN"
            else (
                "人机对战"
                if mode in "COMPUTER"
                else (
                    "残局挑战"
                    if mode == "END"
                    else "网络联机" if mode == "SERVER" else "AI测试"
                )
            )
        )
    )
    GUI.Window.root.title("中国象棋 - %s" % mode)
    GUI.game.player = None
    GUI.Window.tip("— 提示 —\n游戏模式已更新\n为“%s”模式" % mode)
    switch()
    if GUI.game.mode in "COMPUTER END" and not GUI.game.first:
        GUI.Window.root.after(
            500, Thread(target=lambda: GUI.Window.AImove("#000000"), daemon=True).start
        )


def revoke(flag: bool = False) -> None:
    """撤销（悔棋）"""
    import GUI

    if flag or (GUI.game.player and GUI.game.mode in "LOCAL" and GUI.game.index >= 0):
        if GUI.game.choose:
            GUI.game.choose.virtual_delete()
            GUI.game.choose.highlight(False, inside=False)
            GUI.game.choose = None
        (
            o,
            pos,
            v,
        ) = GUI.game.cache[GUI.game.index]
        m = GUI.game.chesses[pos[1]][pos[0]]
        if o:
            color = "#FF0000" if o in "帥仕相馬車砲兵" else "#000000"
            GUI.Chess(o, *pos, color)
        else:
            GUI.game.chesses[pos[1]][pos[0]] = None
        m.move(False, *v, True)
        GUI.game.index -= 1
        switch()
        statistic(Revoke=1)
    elif (
        GUI.game.mode in "COMPUTER END"
        and GUI.game.player == "玩家"
        and GUI.game.index >= 0
    ):
        revoke(True)
        GUI.Window.root.after(600, revoke, True)
        statistic(Revoke=-1)
    else:
        GUI.Window.tip("— 提示 —\n当前模式或状态下\n无法进行悔棋操作！")
        GUI.Window.root.bell()


def recovery(flag: bool = False) -> None:
    """恢复（悔棋）"""
    import GUI

    if flag or (
        GUI.game.player
        and GUI.game.mode == "LOCAL"
        and -1 <= GUI.game.index < len(GUI.game.cache) - 1
    ):
        if GUI.game.choose:
            GUI.game.choose.virtual_delete()
            GUI.game.choose.highlight(False, inside=False)
            GUI.game.choose = None
        GUI.game.index += 1
        (
            o,
            pos,
            v,
        ) = GUI.game.cache[GUI.game.index]
        GUI.game.chesses[pos[1] + v[1]][pos[0] + v[0]].move(bool(o), -v[0], -v[1], True)
        GUI.game.chesses[pos[1] + v[1]][pos[0] + v[0]] = None
        switch()
        statistic(Recovery=1)
    elif (
        GUI.game.mode in "COMPUTER END"
        and GUI.game.player == "玩家"
        and -1 <= GUI.game.index < len(GUI.game.cache) - 1
    ):
        recovery(True)
        GUI.Window.root.after(600, recovery, True)
        statistic(Recovery=-1)
    else:
        GUI.Window.tip("— 提示 —\n当前模式或状态下\n无法进行撤销悔棋操作！")
        GUI.Window.root.bell()
