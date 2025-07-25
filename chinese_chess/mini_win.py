from json import load
from os import listdir
from tkinter import Event
import tkintertools as tkt
from constants import (VOICE_BUTTON, SCREEN_HEIGHT, SCREEN_WIDTH, STATISTIC_DICT , S)
from configure import STATISTIC_PATH, config, configure
from winsound import PlaySound, SND_ASYNC
from tools import open_file

def logo(canvas: tkt.Canvas) -> None:
    """ 给画布加上标志背景 """
    x, y, color = canvas.width[1]//2 + 10*S, canvas.height[1]//2, '#DDD'
    canvas.create_text(x-100*S, y-20*S, text='中', fill=color, font=('华文行楷', round(115*S)))
    canvas.create_text(x-35*S, y+35*S, text='国', fill=color, font=('华文行楷', round(100*S)))
    canvas.create_text(x+35*S, y-35*S, text='象', fill=color, font=('华文行楷', round(75*S)))
    canvas.create_text(x+80*S, y+45*S, text='棋', fill=color, font=('华文行楷', round(85*S)))

class MiniWin:
    """ 小窗口 """
    def __init__(self, root: tkt.Tk, title: str, width: int, height: int) -> None:
        self.toplevel = tkt.Toplevel(
            root, title, int(width*S), int(height*S),
            (SCREEN_WIDTH - tkt.S * width * S)//2,
            (SCREEN_HEIGHT - tkt.S * height * S)//2)
        self.toplevel.resizable(False, False)
        self.toplevel.transient(root)
        self.canvas = tkt.Canvas(self.toplevel, width*S, height*S)
        self.canvas.place(x=0, y=0)

class HelpWin(MiniWin):
    """ 帮助窗口 """
    def __init__(self, root: tkt.Tk) -> None:
        super().__init__(root, '帮助', 400, 300)

        logo(self.canvas)
        self.canvas.create_rectangle(-1, 265*S, 401*S, 301*S, width=0, fill='#F1F1F1')
        self.canvas.create_line(10*S, 40*S, 200*S, 40*S, width=round(2*S))

        self.page = self.canvas.create_text(200*S, 282*S, font=('楷体', round(12*S)))
        self.title = self.canvas.create_text(10*S, 20*S, font=('楷体', round(20*S)), anchor='w')
        self.text = self.canvas.create_text(10*S, 50*S, anchor='nw', font=('楷体', round(12*S)))

        self.last = tkt.CanvasButton(
            self.canvas, 5*S, 270*S, 100*S, 25*S, 6*S, '< 上一页', font=('楷体', round(12*S)),
            command=lambda: self.canvas_set(-1))
        self.next = tkt.CanvasButton(
            self.canvas, 295*S, 270*S, 100*S, 25*S, 6*S, '下一页 >', font=('楷体', round(12*S)),
            command=lambda: self.canvas_set(1))
        
        self.last.command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)
        self.next.command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)

        self.data_list = []
        self.ind = -1
        with open('help.md', 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line.startswith('##'):
                    self.ind += 1
                    self.data_list.append([line[3:].rstrip(), ''])
                else:
                    self.data_list[self.ind][1] += HelpWin.text_limit(line, 22)

        self.ind = 0
        self.canvas_set(0)
    
    @staticmethod
    def text_limit(string: str, length: int) -> str:
        """ 文本单行长度限制 """
        out: str = ' '*4
        for i, s in enumerate(string):
            out += s
            if not (i+2) % length:
                out += '\n'
        return out.rstrip()+'\n'

    def canvas_set(self, delta: int) -> None:
        """ 画布设定 """
        self.ind += delta
        self.canvas.itemconfigure(
            self.page, text=f'{self.ind + 1}/{len(self.data_list)}')
        self.canvas.itemconfigure(self.title, text=self.data_list[self.ind][0])
        self.canvas.itemconfigure(self.text, text=self.data_list[self.ind][1])
        self.last.set_live(self.ind > 0)
        self.next.set_live(self.ind < len(self.data_list) - 1)
    
class StatisticWin(MiniWin):
    """ 统计数据窗口 """
    def __init__(self, root: tkt.Tk) -> None:
        super().__init__(root, '统计数据', 400, 300)
        logo(self.canvas)
        key_text, value_text = '', ''
        with open(STATISTIC_PATH, 'r', encoding='utf-8') as data:
            for key, value in load(data).items():
                key_text += '%s:\n' % STATISTIC_DICT[key]
                value_text += '%d\n' % value
        self.canvas.create_text(20*S, 4*S, text=key_text, font=('楷体', round(12*S)), anchor='nw')
        self.canvas.create_text(380*S, 4*S, text=value_text, font=('楷体', round(12*S)), anchor='ne', justify='right')

class LibraryWin(MiniWin):
    """ 棋局库 """
    def __init__(self, root):
        super().__init__(root, '棋局库', 300, 393)

        self.path_ = self.path = './data'
        self.info = tkt.CanvasLabel(self.canvas, 5*S, 5*S, 200*S, 20*S, 5*S, font=('楷体', 10), justify='left')
        self.back = tkt.CanvasButton(self.canvas, 210*S, 5*S, 80*S, 20*S, 5*S, '←后退', font=('楷体', round(12*S)),
            command=lambda: self.canvas_set(self.path_.rsplit('/', 1)[0]))
        self.back.command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)
        self.content = tkt.Canvas(self.toplevel, int(290*S), int(357*S))
        self.content.configure(highlightthickness=1, highlightbackground='grey')
        self.content.bind('<MouseWheel>', self.scroll)
        self.content.place(x=5*S, y=30*S)
        self.canvas_set(self.path)
            
    def scroll(self, event: Event) -> None:
        """ 上下移动画布 """
        if (event.delta < 0 and self.content.pos <= 10) or (event.delta > 0 and self.content.pos >= self.content.length):
            return
        key = 1 if event.delta > 0 else -1
        self.content.pos += key
        for widget in self.content.widget():
            tkt.move(self.content, widget, 0, 35*key*S, 300, 'smooth', 30)

    def canvas_set(self, path: str) -> None:
        """ 画布设定 """
        if path.endswith('.fen'):
            self.toplevel.destroy()
            return open_file(path)
        elif path[-4:] == 'data':
            self.back.set_live(False)
        else:
            self.back.set_live(True)

        self.path_ = path
        self.info.configure(text=path.replace('./data', '.'))

        path_list = listdir(path)
        self.content.pos = self.content.length = len(path_list)

        for widget in self.content.widget():
            widget.destroy()

        for i, file in enumerate(path_list):
            tkt.CanvasButton(
                self.content, 5*S, (5+i*35)*S, 280*S, 30*S, 5*S,
                file.replace('.fen', ''),
                command=lambda path=path, file=file: self.canvas_set(f'{path}/{file}')
            ).command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)

class SettingWin(MiniWin):
    """ 设置窗口"""
    def __init__(self, root) -> None:
        super().__init__(root, '游戏设置', 400, 300)
        logo(self.canvas)
        self.canvas.create_rectangle(-1, 265*S, 401*S, 301*S, width=0, fill='#F1F1F1')
        self.canvas.create_text(20*S, 20*S, text='窗口缩放系数（重启生效）', font=('楷体', round(12*S)), anchor='w')
        self.canvas.create_text(20*S, 50*S, text='窗口自动缩放（重启生效）', font=('楷体', round(12*S)), anchor='w')
        self.canvas.create_text(20*S, 80*S, text='棋子可走显示', font=('楷体', round(12*S)), anchor='w')
        self.canvas.create_text(20*S, 110*S, text='AI最大搜索深度', font=('楷体', round(12*S)), anchor='w')
        self.canvas.create_text(20*S, 140*S, text='AI搜索算法', font=('楷体', round(12*S)), anchor='w')
        self.canvas.create_text(20*S, 170*S, text='和棋判定回合数', font=('楷体', round(12*S)), anchor='w')

        self.scale = tkt.CanvasEntry(self.canvas, 220*S, 10*S, 100*S, 20*S, 5*S, justify='center', font=('楷体', round(12*S)), color_fill=tkt.COLOR_NONE)
        self.scale.set(str(config['scale']))
        self.scale.cursor_flash()

        self.auto_scale = tkt.CanvasButton(
            self.canvas, 220*S, 40*S, 80*S, 20*S, 5*S, str(config['auto_scale']), font=('楷体', round(12*S)),
            command=lambda: self.auto_scale.configure(text='True' if self.auto_scale.value == 'False' else 'False'), color_fill=tkt.COLOR_NONE)
        self.auto_scale.command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)

        self.info = tkt.CanvasButton(
            self.canvas, 130*S, 70*S, 80*S, 20*S, 5*S, str(config['virtual']), font=('楷体', round(12*S)),
            command=lambda: self.info.configure(text='True' if self.info.value == 'False' else 'False'), color_fill=tkt.COLOR_NONE)
        self.info.command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)

        self.level = tkt.CanvasEntry(self.canvas, 140*S, 100*S, 100*S, 20*S, 5*S, justify='center', font=('楷体', round(12*S)), color_fill=tkt.COLOR_NONE)
        self.level.set(str(config['level']))
        self.level.cursor_flash()

        self.peace = tkt.CanvasEntry(self.canvas, 140*S, 160*S, 100*S, 20*S, 5*S, justify='center', font=('楷体', round(12*S)), color_fill=tkt.COLOR_NONE)
        self.peace.set(str(config['peace']))
        self.peace.cursor_flash()

        self.ai = tkt.CanvasButton(self.canvas, 110*S, 130*S, 200*S, 20*S, 5*S,
                              "极小极大搜索" if config[
                                  'algo'] == 1 else "alpha-beta 剪枝" if config['algo'] == 2 else "alpha-beta 剪枝(C++实现)",
                              font=('楷体', round(12*S)), color_fill=tkt.COLOR_NONE,
                              command=lambda: self.ai.configure(text=("极小极大搜索" if self.ai.value == "alpha-beta 剪枝(C++实现)" else "alpha-beta 剪枝" if ai.value == "极小极大搜索" else "alpha-beta 剪枝(C++实现)")))
        self.ai.command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)

        tkt.CanvasButton(self.canvas, 314*S, 271*S, 80*S, 23*S, 6*S, '保存', font=('楷体', round(12*S)), command=self.save
                         ).command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)
        tkt.CanvasButton(self.canvas, 228*S, 271*S, 80*S, 23*S, 6*S, '恢复默认', font=('楷体', round(12*S)), command=self.default
                         ).command_ex['press'] = lambda: PlaySound(VOICE_BUTTON, SND_ASYNC)
    
    def save(self) -> None:
        """ 保存设定 """
        configure(
            scale=float(self.scale.get()),
            virtual=eval(self.info.value),
            auto_scale=eval(self.auto_scale.value),
            level=int(self.level.get()),
            peace=int(self.peace.get()),
            algo=1 if self.ai.value == "极大极小搜索" else 2 if self.ai.value == "alpha-beta 剪枝" else 0)
        self.toplevel.destroy()
    
    def default(self) -> None:
        """ 默认设定 """
        self.scale.set('1')
        self.scale.cursor_flash()
        self.level.set('4')
        self.level.cursor_flash()
        self.peace.set('60')
        self.peace.cursor_flash()
        self.info.configure(text='True')
        self.auto_scale.configure(text='True')
        self.ai.configure(text="alpha-beta 剪枝(C++实现)")