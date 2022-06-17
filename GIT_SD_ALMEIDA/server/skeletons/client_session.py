from threading import Thread
import logging
import server as _server
import skeletons
from sockets import Socket


class ClientSession(Thread):
    """Maintains a session with the client"""

    def __init__(self, shared_state: skeletons.SharedServerState, client_socket: Socket):
        """
        Constructs a thread to hold a session with the client

        :param shared_state: The server's state shared by threads
        :param client_socket: The client's socket
        """
        Thread.__init__(self)
        self._shared_state = shared_state
        self._client_connection = client_socket
        self.players = []

    def start_game(self):

        if len(self.players) == 2:
            self._client_connection.send_int(_server.GAME_FULL, 1)
        elif len(self.players) == 1:
            has_started = self._shared_state.server.start_game()
            self._client_connection.send_int(has_started, 1)

        elif len(self.players) == 0:
            self._client_connection.send_int(False, 1)



    def make_move(self):
        move = self._client_connection.receive_str()
        makemove = self._shared_state.server.make_move(move)
        self._client_connection.send_str(makemove)

    def add_player(self):
        player = self._client_connection.receive_str()
        addplayer = self._shared_state.server.addplayer(player)
        self._client_connection.send_int(addplayer, 1)

    def is_player_turn(self):
        player = self._client_connection.receive_str()
        is_turn = self._shared_state.server.game.is_turn(player)
        self._client_connection.send_int(is_turn, 1)

    def game_map(self):
        showmap = self._shared_state.server.showgrid()
        self._client_connection.send_str(showmap)

    def setup_map(self):
        response = self._client_connection.receive_str()
        size = int(response.split("-")[0])
        n_mines = int(response.split("-")[1])
        self._shared_state.server.setup_map(size,n_mines)
        self._client_connection.send_int(True,1)

    def get_status(self):
        self._shared_state.server.get_status()
        return self._client_connection.send_int(1)

    """def add(self) -> None:
        a = self.communication.receive_int(_server.INT_SIZE)
        b = self.communication.receive_int(_server.INT_SIZE)
        result = _server.Server.add(a, b)
        self.communication.send_int(result, _server.INT_SIZE)

    def sym(self) -> None:
        a = self.communication.receive_int(_server.INT_SIZE)
        result = _server.Server.sym(a)
        self.communication.send_int(result, _server.INT_SIZE)

    # Adding new command: subtraction...
    def subtract(self) -> None:
        a = self.communication.receive_int(_server.INT_SIZE)
        b = self.communication.receive_int(_server.INT_SIZE)
        result = _server.Server.subtract(a, b)
        self.communication.send_int(result, _server.INT_SIZE)"""
    """
    def handle(self):
        last_request = False
        with _server.lock:
            _server.nr_threads = _server.nr_threads + 1
        logging.info("Handle server thread started. Number of active threads: " + str(_server.nr_threads))

        while not last_request:
            keep_running, last_request = self.dispatch_request()
            # Get data from the current thread ...
            cur_thread = Thread.current_thread()
            logging.debug("Data received from thread:" + cur_thread.name)
            # self.current_connection.close()
        with _server.lock:
            _server.nr_threads = _server.nr_threads - 1
        logging.info("Handle server thread stopped. Number of active threads: " + str(_server.nr_threads))
    """

    def run(self):
        """Maintains a session with the client, following the established protocol"""
        with self._client_connection as client:
            logging.debug("Client " + str(client.peer_addr) + " just connected")
            last_request = False
            while not last_request:
                last_request = self.dispatch_request()
            logging.debug("Client " + str(client.peer_addr) + " disconnected")
            self._shared_state.remove_client(self._client_connection)
            self._shared_state.concurrent_clients.release()

    def dispatch_request(self) -> (bool, bool):
        request_type = self._client_connection.receive_str()
        last_request = False
        # if request_type == _server.ADD_OP:
        #     self.add()
        # elif request_type == _server.SYM_OP:
        #     self.sym()
        # elif request_type == _server.SUB_OP:
        #     self.subtract()
        # elif request_type == _server.BYE_OP:
        #     last_request = True
        if request_type == _server.START_GAME_OP:
            self.start_game()
        elif request_type == _server.ADD_PLAYER_OP:
            self.add_player()
        elif request_type == _server.MAP_OP:
            self.game_map()
        elif request_type == _server.MAP_SETUP_OP:
            self.setup_map()
        # elif request_type == _server.TURN_OP:
        #     self.is_player_turn()
        elif request_type == _server.MOVE_OP:
            self.make_move()
        elif request_type == _server.STOP_SERVER_OP:
            last_request = True
        return last_request

