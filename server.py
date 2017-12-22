import select
import socket
import sys
import jim
from config.params import *
from console import Params
from db.server_repo import ServerRepo


class Handler:
    def __init__(self):
        self._repo = ServerRepo()

    def run_action(self, request):
        if request.action == 'presence':
            self._repo.add_client(request.user_account_name)
            return jim.success()
        elif request.action == 'quit':
            return jim.success()
        elif request.action == 'msg':
            return jim.success()
        elif request.action == 'get_contacts':
            count = self._repo.get_contacts()
            contacts = self._repo.get_contact_list()
            responses = [jim.success(response=202, quantity=count)]
            for contact in contacts:
                account_name = contact.name
                responses.append(jim.Message(action='contact_list', account_name=account_name))
            return responses
        elif request.action == 'contact_list':
            return jim.success()
        elif request.action == 'add_contact':
            return jim.success()
        elif request.action == 'del_contact':
            return jim.success()
        elif request.action == 'error':
            return jim.error(request.msg)
        else:
            return jim.error('Action is not available')


class Server:
    def __init__(self, address):
        self.__server = socket.socket()
        self.__server.bind(address)
        self.__server.listen(WORKERS)
        self.__server.settimeout(0.2)
        self.__handler = Handler()
        self.__clients = []
        self.__in = []
        self.__out = []

    def listen(self):
        while True:
            try:
                client, address = self.__server.accept()
                presence = jim.receive(client)[0]
                response = self.__handler.run_action(presence)
                jim.send(client, response)
            except OSError as e:
                pass
            else:
                print('Increase connection until {} with {}'.format(len(self.__clients) + 1, address))
                self.__clients.append(client)
            finally:
                self.__io()

    def __io(self):
        r = []
        w = []
        try:
            r, w, e = select.select(self.__clients, self.__clients, [], 0)
        except Exception as e:
            print('Exception until I/O select - {}'.format(e.args))
        self.__input(r)
        self.__process()
        self.__output(w)

    def __input(self, clients):
        for c in clients:
            try:
                msg = jim.receive(c)
                self.__in.extend(msg)
            except:
                self.__remove_client(c)

    def __process(self):
        while len(self.__in):
            msg = self.__in.pop()
            responses = self.__handler.run_action(msg)
            if isinstance(responses, jim.Message):
                self.__out.append(responses)
            else:
                while len(responses):
                    self.__out.append(responses.pop())

    def __output(self, clients):
        while len(self.__out):
            msg = self.__out.pop()
            for c in clients:
                try:
                    jim.send(c, msg)
                except:
                    self.__remove_client(c)

    def __remove_client(self, c):
        c.close()
        self.__clients.remove(c)


if __name__ == '__main__':
    params = Params(sys.argv)
    s = Server(params.server_host)
    s.listen()
