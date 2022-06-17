from game.minesweeper import MineSweeper


class Server:


    def __init__(self):
        self.game = MineSweeper()

    """
    A very simple distributed server server.
    """

    def start_game(self):
        return self.game.startgame()

    def setup_map(self,size, n_mines):
        self.game.size = size
        self.game.n_mines = n_mines
        return True

    def make_move(self, move):
        return self.game.makemove(move)

    def showgrid(self):
        return self.game.showgrid()

    def addplayer(self, player):
        return self.game.addplayer(player)

    def removeplayer(self, player):
        return self.game.removeplayer(player)

    def is_turn(self, player):
        return self.game.is_turn(player)

    def get_players(self):
        return self.game.players

"""
    @staticmethod
    def sym(a: int) -> int:
        return -a
#   Adding a new method...
    @staticmethod
    def subtract(a: int, b: int) -> int:
        return a - b
"""
