import sys
import socket
from helpers import console
from config.params import *
from app.console.client import Client as ConsoleClient
from app.desktop.client import Client as GuiClient


class Client:
    def __init__(self, address, controller):
        self.__sock = socket.socket()
        self.__sock.connect(address)
        self.__controller = controller

    def listen(self):
        parcel = self.__sock.recv(MESSAGE_SIZE)
        return self.__controller.get_response(parcel)

    def send(self):
        self.__sock.send(self.__controller.get_request())

    def close(self):
        self.__sock.close()


if __name__ == '__main__':
    host = console.host_params(sys.argv, True)
    handler = ConsoleClient() if console.is_console_mode(sys.argv) else GuiClient()
    client = Client(host, handler)
    while True:
        client.send()
        print(client.listen())
