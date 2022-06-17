import skeletons
from server import Server, PORT


def main():
    skeletons.Server(PORT, Server()).run()


main()
