# Chinese Chess (Xiangqi)

🌐 [English](#chinese-chess-xiangqi) | [简体中文](#简体中文)

---

Chinese Chess (Xiangqi) is a traditional two-player strategy game that originated in China. Similar to international chess, it has a long and rich history. Due to its simple tools and engaging gameplay, it is widely popular throughout China and many other regions.

Xiangqi uses a square-grid board with 32 circular pieces in total—16 for each side (red and black). Pieces are placed and moved on the intersections (not inside the squares). Players take turns to move their pieces, and the player who checkmates the opponent's general (帥/将) wins the game.

## 🎮 How to Play?

### Game Rules

[Click here to learn the rules](./chinese_chess/help-en.md)

### Game Modes

The game features three basic modes, one extended mode, and one hidden (debug) mode:

- **Player vs AI**: Battle against the computer.
- **Two-player Local**: Two players share the same device to play.
- **Online Mode**: Play over the network with another player on a different device.
- **Endgame Challenge (Extended Mode)**: Load a Xiangqi file or choose from the preset endgame library via the menu to start an endgame scenario.
- **Test Mode (Hidden)**: Two AIs play against each other for testing purposes. To activate, close the "Mode Selection" window and press `Ctrl + T`.

Now, start your own battlefield and enjoy the fight!

## 📂 File Structure

### Source Code Files

1. `AI.py`:              AI logic
2. `configure.py`:       Configuration settings
3. `constants.py`:       Game constants
4. `GUI.py`:             Graphical user interface
5. `LAN.py`:             LAN communication module
6. `rule.py`:            Game rule engine
7. `tkintertools.py`:    Tkinter GUI helper utilities
8. `tools.py`:           General-purpose utility functions

### Resource Files

1. `chinese_chess_config.json`:    Configuration data
2. `chinese_chess_statistic.json`: Gameplay statistics
3. `help.md`:        Help and rules (in Chinese)
4. `audio/*.wav`:    Sound effects
5. `data/`:          Endgame libraries

## 🔧 How to Build?

> This project is written in Python and C++.

### Build C++ Lib

#### Prerequisites

- Visual Studio 2022

#### Steps

1. Open `chinese_chess.sln`
2. build `alpha_beta_search`

### Build Python GUI

#### Prerequisites

- Python 3.7+
- `tkinter`
- `pyinstaller`

#### Steps

Run `install.bat`

---

Enjoy the game, and feel free to contribute or open issues!

## 简体中文

🌐 [English](#chinese-chess-xiangqi) | [简体中文](#简体中文)

---

中国象棋是起源于中国的一种棋类似于国际象棋，属于二人对抗性游戏的一种，在中国有着悠久的历史。由于用具简单，趣味性强，成为流行极为广泛的棋艺活动。

中国象棋使用方形格状棋盘，圆形棋子共有32个，红黑二色各有16个棋子，摆放和活动在交叉点上。双方交替行棋，先把对方的将（帥）“将死”的一方获胜。

## 🎮 如何游玩？

### 游戏规则

[请看这里](./chinese_chess/help.md)

### 游戏模式

游戏分为三个基本模式、一种扩展模式和一种隐藏（调试）模式：

- 人机模式：玩家和电脑对局
- 双人模式：两个玩家在同一台设备上对局
- 联机模式：两个玩家在两台设备上对局
- 残局模式（扩展）：导入象棋文件，或者点击菜单栏内的棋局库，即可开启“残局挑战”模式
- 测试模式（隐藏）：两个电脑之间的对局，用于调试。启动程序时，关闭“选择模式”窗口并按下“Ctrl+t”组合键以开启

最后，开始一场属于你的战争吧！

## 📂 文件结构

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

1. chinese_chess_config.json:    配置信息
2. chinese_chess_statistic.json: 统计数据
3. help.md:        帮助文本
4. audio/*.wav:    音效文件
5. data            棋局库

## 🔧 如何构建?

> 这个项目使用Python和C++编写。

### 构建C++库

#### 需要

- Visual Studio 2022

### 步骤

1. 打开`chinese_chess.sln`
2. 构建`alpha_beta_search`

### 构建Python GUI

#### 需要

- Python3.7+
- `tkinter`
- `pyinstaller`

### 步骤

运行`install.bat`

---
祝您玩得愉快，欢迎参与贡献或提交问题反馈!
