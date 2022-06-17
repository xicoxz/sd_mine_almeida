from stubs import Server, PORT, SERVER_ADDRESS
from ui.client import Client


def main():
    server = Server(SERVER_ADDRESS, PORT)
    client = Client(server)
    client.run()


main()
