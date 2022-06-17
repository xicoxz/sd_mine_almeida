import server
import logging

import skeletons
import sockets


class Server:
    def __init__(self, port: int, math_server: server.Server) -> None:
        """
        Creates a client given the server server to use
        :param port: The math server port of the host the client will use
        """
        super().__init__()
        self._state = skeletons.SharedServerState(math_server, port)
        logging.basicConfig(filename=server.LOG_FILENAME,
                            level=server.LOG_LEVEL,
                            format='%(asctime)s (%(levelname)s): %(message)s')

    def run(self) -> None:
        """
        Runs the server server until the client sends a "terminate" action
        """

        with sockets.Socket.create_server_socket(self._state.port, server.ACCEPT_TIMEOUT) as server_socket:
            logging.info("Waiting for clients to connect on port " + str(self._state.port))

            while self._state.keep_running:
                self._state.concurrent_clients.acquire()
                client_socket = server_socket.accept()
                if client_socket is not None:
                    self._state.add_client(client_socket)
                    skeletons.ClientSession(self._state, client_socket).start()
                else:
                    self._state.concurrent_clients.release()

            logging.info("Waiting for clients to terminate...")

        logging.info("Server stopped")
