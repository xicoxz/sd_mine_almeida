from stubs import Server
import stubs as stubs
import time


class Client:
    def __init__(self, server: Server) -> None:
        """
        Creates a client given the stubs stubs to use
        :param math_server: The math stubs the client will use
        """
        self._server = server

    def stop_server(self):
        self._server.stop_server()

    def run(self) -> None:
        """Executes a simple client"""
        player_name = input("Nome do jogador:")
        has_started = self._server.start_game()
        added = self._server.addplayer(player_name)
        if not has_started:
            size = input("Tamanho do tabuleiro:")
            n_mines = input("Nº de minas:")
            response = self._server.send_setup(size,n_mines)
        # if not has_started:
        #     self._server.sendgrid()
        # print(has_started)
        # if not has_started:
        #     print("É o primeiro jogador, por favor aguarde.")
        #     self._server.addplayer(player_name)

        print("A partida já vai começar.")

        while True:
            # map = self._server.show_map()
            # print(map)
            move = input("Qual a jogada:")
            response = self._server.send_move(move)
            print(response)
            map = self._server.show_map()
            print(map)
            status = self._server.get_status()
            print(status)

            if status == stubs.GAME_WON:
                print("Ganharam!")
            elif status == stubs.GAME_LOST:
                print("Perderam")
            if status != -1:
                break
            if self._server.is_finished():
                break

            """# first interaction with the stubs
            print("First interaction")
            self.add()
            self.sym()

            # second interaction with the stubs
            print("Second interaction")
            self.sym()

            # terminate the server
            self.stop_server()"""

    """def add(self) -> None:

        Asks the user two integer numbers and use the stubs stubs to add them

        print("Add two numbers")
        a = int(input("a: "))
        b = int(input("b: "))
        print("the result is", self._server.add(a, b))

    def sym(self) -> None:

        Asks the user for an integer number and uses the stubs stubs to compute its symmetric

        print("The symmetric of a number")
        a = int(input("a: "))
        print("the result is", self._server.sym(a))

    """
