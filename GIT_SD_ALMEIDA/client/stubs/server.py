import socket
import stubs as stubs
from sockets.sockets_mod import Socket


class Server:

    """
    A math control_client_stubs stub (client side).
    """

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.current_connection = Socket.create_client_socket(host, port)

    def has_other_player(self):
        self.current_connection.send_str(stubs.HAS_PLAYER_OP)
        return self.current_connection.receive_int(1)

    def show_map(self):
        self.current_connection.send_str(stubs.MAP_OP)
        return self.current_connection.receive_str()

    def send_setup(self,size,n_mines):
        self.current_connection.send_str(stubs.MAP_SETUP_OP)
        self.current_connection.send_str(size+"-"+n_mines)
        return self.current_connection.receive_str()

    def get_status(self):
        self.current_connection.send_str(stubs.STATUS_OP)
        return self.current_connection.receive_int(1)

    def send_move(self, move: str):
        self.current_connection.send_str(stubs.MOVE_OP)
        self.current_connection.send_str(move)
        return self.current_connection.receive_str()

    def is_finished(self):
        self.current_connection.send_str(stubs.GAME_FINISH_OP)
        return self.current_connection.receive_int(1)

    def start_game(self):
        self.current_connection.send_str(stubs.START_GAME_OP)
        return self.current_connection.receive_int(1)


    def stop_server(self):
        self.current_connection.send_str(stubs.STOP_SERVER_OP)
        self.current_connection.close()

    def addplayer(self, player):
        self.current_connection.send_str(stubs.ADD_PLAYER_OP)
        self.current_connection.send_str(player)
        return self.current_connection.receive_str()






"""

    def add(self, a: int, b: int) -> int:

        Read two integers from the current open connection, adds them up,
        and send the result back through the connection.
 
        self.current_connection.send_str(stubs.ADD_OP)
        self.current_connection.send_int(a, stubs.INT_SIZE)
        self.current_connection.send_int(b, stubs.INT_SIZE)
        return self.current_connection.receive_int(stubs.INT_SIZE)

    def sym(self, a: int) -> int:

        Read one integer from the current open connection, computes its
        symmetric, and send the result back to the connection
        
        self.current_connection.send_str(stubs.SYM_OP)
        self.current_connection.send_int(a, stubs.INT_SIZE)
        return self.current_connection.receive_int(stubs.INT_SIZE)

    def bye(self):
        self.current_connection.send_str(stubs.BYE_OP)
        self.current_connection.close()
        """

