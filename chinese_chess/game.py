class GameState:
    """全局变量"""

    def __init__(self):
        self.mode = None  # 当前游戏模式
        self.timer = 0  # 计时判断时间戳
        self.count = 0  # 未吃棋回合计数（和棋判定需要）
        self.index = -1  # 当前缓存索引
        self.first = None  # 当前先手方
        self.player = None  # 当前操作方
        self.choose = None  # 当前选中棋子
        self.cache = []  # 走棋缓存列表
        self.chesses = [  # 棋盘列表
            [None] * 9 for _ in range(10)
        ]  # type: list[list[Chess | None]]

    def select_piece(self, x, y):
        piece = self.board[y][x]
        if piece and piece.color == self.current_player:
            self.selected_piece = piece
            return True
        return False

    def reset(self):
        self.__init__()


game = GameState()
