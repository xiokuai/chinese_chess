__version__ = "1.2.1"
__author__ = "李悟/梁晨轩"
__update__ = "2025/9/20"
__license__ = "GPL-3.0"
__website__ = "https://github.com/xiokuai/chinese_chess"
LOG_FILE = "error.log"

import tkinter as tk
import traceback
import os
import datetime
from tkinter import messagebox
import sys


def show_error_popup(exc_type, exc_value, exc_traceback):
    # 格式化完整堆栈
    tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(tb_str)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"==== {datetime.datetime.now()} ====\n")
        f.write(tb_str + "\n")

    root = tk.Tk()
    root.withdraw()

    short_msg = f"程序发生错误：{exc_type.__name__}: {exc_value}\n详细错误已保存到日志文件 {os.path.abspath(LOG_FILE)}"
    messagebox.showerror("程序错误", short_msg)
    root.destroy()


if __name__ == "__main__":
    sys.excepthook = show_error_popup

    from configure import statistic
    from GUI import Window

    # 更新统计数据
    statistic(Launch=1)
    # 启动主窗口
    Window()
