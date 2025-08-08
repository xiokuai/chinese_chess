# 版本号
__version__ = '1.1.0'
# 作者
__author__ = '李悟/梁晨轩'
# 更新日期
__update__ = '2025/7/12'

import tkinter as tk
from tkinter import messagebox
import sys

def show_error_popup(exc_type, exc_value, exc_traceback):
    # TODO: Logging
    print(exc_traceback)
    root = tk.Tk()
    root.withdraw()
    short_msg = f"程序发生错误：{exc_type.__name__}: {exc_value}\n位于{exc_value.__traceback__.tb_frame.f_code.co_filename}的第{exc_value.__traceback__.tb_lineno}行"
    messagebox.showerror("程序错误", short_msg)
    root.destroy()

if __name__ == '__main__':
    sys.excepthook = show_error_popup

    from configure import statistic
    from GUI import Window

    # 更新统计数据
    statistic(Launch=1)
    # 启动主窗口
    Window()
