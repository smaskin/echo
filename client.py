import sys
import socket
from helpers import console
from message import Message
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
        pack = self.__sock.recv(MESSAGE_SIZE)
        return Request(pack)

    def send(self):
        text = input('Введите сообщение: ')
        message = Message(text)
        self.__sock.send(message.pack())

    def close(self):
        self.__sock.close()


if __name__ == '__main__':
    client = Client(console.host_params(sys.argv, True))
    while True:
        if console.is_write_mode(sys.argv):
            client.send()
        print(client.listen().text)
