import sys
import socket
import select
from helpers import console
from request import Request
from response import Response
from config.params import *


class Server():
    """
    Класс Сервер - базовый класс сервера мессенджера;
    может иметь разных потомков - работающих с потоками или выполняющих асинхронную обработку.
    """
    def __init__(self, address):
        self.__server = socket.socket()
        self.__server.bind(address)
        self.__server.listen(WORKERS)
        self.__server.settimeout(0.2)
        self.__clients = []
        self.__requests = []

    def listen(self):
        while True:
            try:
                client, address = self.__server.accept()
            except OSError as e:
                pass
            else:
                print('Получен запрос на соединение от {}'.format(address))
                self.__clients.append(client)
            finally:
                self.__io()

    def __io(self):
        r = []
        w = []
        try:
            r, w, e = select.select(self.__clients, self.__clients, [], 0)
        except Exception as e:
            print('Исключение при опросе клиентов - {}'.format(e.args))
        self.__input(r)
        self.__output(w)

    def __input(self, clients):
        for c in clients:
            try:
                pack = c.recv(MESSAGE_SIZE)
                self.__requests.append(Request(pack))
            except:
                self.__remove_client(c)

    def __output(self, clients):
        while len(self.__requests):
            request = self.__requests.pop()
            response = Response(request)
            print('Ответ {} клиентам, запроса "{}".'.format(len(clients), request.text))
            for c in clients:
                try:
                    c.send(response.pack())
                except:
                    self.__remove_client(c)

    def __remove_client(self, c):
        c.close()
        self.__clients.remove(c)


if __name__ == '__main__':
    host = console.host_params(sys.argv)
    s = Server(host)
    s.listen()
