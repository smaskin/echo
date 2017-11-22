import sys
import socket
from helpers import console
from config.params import *
from request import Request


class Client:
    """
    Класс Клиент - класс, реализующий клиентскую часть системы.
    """
    def __init__(self, address):
        self.__sock = socket.socket()
        self.__sock.connect(address)

    def listen(self):
        return self.__sock.recv(MESSAGE_SIZE)

    def send(self):
        text = input('Введите сообщение: ')
        request = Request(text=text)
        self.__sock.send(bytes(request))

    def close(self):
        self.__sock.close()


if __name__ == '__main__':
    client = Client(console.host_params(sys.argv, True))
    while True:
        if console.is_write_mode(sys.argv):
            client.send()
        print(client.listen())
