"""
* main.py:            程序入口

### 源代码文件

1. AI.py:              电脑算法
2. configure.py:       配置设定
3. constants.py:       所有常量
4. GUI.py:             图形界面
5. LAN.py:             局域网功能
6. rule.py:            游戏规则控制
7. tkintertools.py:    图形界面辅助模块
8. tools.py:           工具函数

### 资源文件

1. chnese_chess_config.json:    配置信息
2. chenese_chess_statistic.json: 统计数据
3. help.md:        帮助文本
4. audio/*.wav:    音效文件
5. data            棋局库
"""

# 版本号
__version__ = '1.1.0'
# 作者
__author__ = '李悟/梁晨轩'
# 更新日期
__update__ = '2025/7/12'

if __name__ == '__main__':
    from configure import statistic
    from GUI import Window

    # 更新统计数据
    statistic(Launch=1)
    # 启动主窗口
    Window()
