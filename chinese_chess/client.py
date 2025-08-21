"""
客户端功能
"""

import json
from threading import Thread
import websocket
from game import game
import rule
from rule import modechange
from sound import play_sound_async
import tkintertools as tkt
from constants import S, VOICE_BUTTON
from configure import config
import requests


class WebSocketClient:
    global_ws: websocket.WebSocketApp | None = None

    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.canvas = tkt.Canvas(
            self.toplevel, 400 * S, 150 * S, bg="#FFFFFF", expand=False
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            -1, 115 * S, 401 * S, 151 * S, width=0, fill="#F1F1F1"
        )

        # 创建输入框让用户输入服务器 URI
        self.create_button = tkt.CanvasButton(
            self.canvas,
            20 * S,
            40 * S,
            80 * S,
            23 * S,
            6 * S,
            text="创建新游戏",
            font=("楷体", round(12 * S)),
            command=self.create,
        )

        self.id_entry = tkt.CanvasEntry(
            self.canvas,
            120 * S,
            40 * S,
            160 * S,
            23 * S,
            5 * S,
            font=("楷体", round(12 * S)),
            justify="center",
            color_fill=tkt.COLOR_NONE,
        )

        # 确认按钮
        self.ok = tkt.CanvasButton(
            self.canvas,
            128 * S,
            121 * S,
            80 * S,
            23 * S,
            6 * S,
            font=("楷体", round(12 * S)),
            text="确认",
            command=lambda: self.start(
                config["server_adress"] + "/ws/" + self.id_entry.value
            ),
        )
        self.ok.command_ex["press"] = lambda: play_sound_async(VOICE_BUTTON)

        # 取消按钮
        self.cancel = tkt.CanvasButton(
            self.canvas,
            214 * S,
            121 * S,
            80 * S,
            23 * S,
            6 * S,
            font=("楷体", round(12 * S)),
            text="取消",
            command=self.close,
        )
        self.cancel.command_ex["press"] = lambda: play_sound_async(VOICE_BUTTON)

        # TODO: 禁用确认按钮直到用户输入内容
        # self.ok.set_live(False)

    def create(self):
        canvas_ = tkt.Canvas(self.toplevel, 400 * S, 150 * S, expand=False)
        canvas_.place(x=0, y=0)
        from GUI import more_set

        more_set(self.toplevel, canvas_)
        last = tkt.CanvasButton(
            canvas_,
            6 * S,
            121 * S,
            80 * S,
            23 * S,
            6 * S,
            font=("楷体", round(12 * S)),
            text=("上一步"),
            command=lambda: (self.toplevel.title(("选择模式")), canvas_.destroy()),
        )
        last.command_ex["press"] = lambda: play_sound_async(VOICE_BUTTON)
        tkt.CanvasButton(
            canvas_,
            214 * S,
            121 * S,
            80 * S,
            23 * S,
            6 * S,
            font=("楷体", round(12 * S)),
            text=("开始"),
            command=lambda: (
                self.request_create(),
                self.toplevel.destroy(),
            ),
        ).command_ex["press"] = lambda: play_sound_async(VOICE_BUTTON)

    # 发送 POST 请求
    def request_create(self):
        code = "".join([str(v.get()) for v in self.toplevel.var_list])
        response = requests.post(
            url="http://" + config["server_adress"] + "/create_game?game_code=" + code
        )

        if response.status_code == 200:
            # 获取返回的 JSON 数据并解析
            response_data = response.json()

            # 获取 game_id
            game_id = response_data.get("game_id", None)

            if game_id:
                print(f"游戏ID: {game_id}")
                self.start(config["server_adress"] + "/ws/" + game_id)
                self.toplevel.destroy()
            else:
                print("返回的 JSON 中没有 game_id")
        else:
            print(f"请求失败，状态码: {response.status_code}")

    def start(self, uri: str):
        self.toplevel.destroy()
        self.uri = "ws://" + uri
        Thread(target=self.connect, daemon=True).start()

    def connect(self):
        websocket.enableTrace(True)
        WebSocketClient.global_ws = websocket.WebSocketApp(
            self.uri,
            on_open=on_open,
            on_message=self.on_message,
            on_error=on_error,
            on_close=on_close,
        )

        WebSocketClient.global_ws.run_forever(
            reconnect=5
        )  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        # rel.signal(2, rel.abort)  # Keyboard Interrupt
        # rel.dispatch()

    @classmethod
    def on_message(cls, ws, message):
        """接收消息"""
        message_data = json.loads(message)
        print(message_data)
        if "game_code" in message_data:
            message_data["game_code"][0] = (
                "0" if message_data["game_code"][0] == "1" else "1"
            )
            modechange("SERVER", "".join(message_data["game_code"]))
        if "msg" in message_data:
            x, y, flag, x_, y_ = message_data["msg"]
            if (x, y) == (x_, y_):
                return
            game.chesses[9 - y][8 - x].move(flag, -x_, -y_)
            rule.switch()

    @classmethod
    def send_message(cls, **kw):
        """单独的发送消息数"""
        cls.global_ws.send(json.dumps(kw, ensure_ascii=False).encode("utf-8"))
        print(f"Message sent: {kw}")

    def close(self) -> None:
        """关闭联机功能"""
        self.flag = True
        self.canvas.destroy()


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")
