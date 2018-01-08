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
            client = self._repo.get_user_by_name(request.client_name)
            contacts = client.contacts
            responses = [jim.success()]
            for contact in contacts:
                responses.append(jim.Message(
                    action='msg',
                    text=request.text,
                    to=contact.name,
                    _from=request.client_name
                ))
            return responses
        elif request.action == 'get_contacts':
            contacts = self._repo.get_contact_list(request.client_name)
            count = len(contacts)
            responses = [jim.success(response=202, quantity=count)]
            for contact in contacts:
                account_name = contact.name
                responses.append(jim.Message(action='contact_list', account_name=account_name))
            return responses
        elif request.action == 'add_contact':
            try:
                self._repo.add_contact(request.client_name, request.user_name)
                return jim.success()
            except:
                return jim.error('Contact does not exist')
        elif request.action == 'del_contact':
            try:
                self._repo.remove_contact(request.client_name, request.user_name)
                return jim.success()
            except:
                return jim.error('Contact does not exist')
        elif request.action == 'error':
            return jim.error('Error action')
        else:
            return jim.error('Action is not available')


class Server:
    def __init__(self, address):
        self.__server = socket.socket()
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind(address)
        self.__server.listen(WORKERS)
        self.__server.settimeout(0.2)
        self.__handler = Handler()
        self.__clients = []
        self.__dispatchers = {}
        self.__names = {}
        self.__in = []
        self.__out = []

    def listen(self):
        while True:
            try:
                client, address = self.__server.accept()
                dispatcher = jim.Dispatcher(client)
                dispatcher.receive()
                dispatcher.process(self.__handler)
                dispatcher.release()
            except OSError as e:
                pass
            else:
                print('Increase connection until {} with {}'.format(len(self.__clients) + 1, address))
                self.__clients.append(client)
                self.__dispatchers[client] = dispatcher
                self.__names[dispatcher.client_name] = client
            finally:
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
                dispatcher = self.__dispatchers[c]
                dispatcher.receive()
                self.__in.append(dispatcher)
            except:
                self.__remove_client(c)

    def __process(self):
        while len(self.__in):
            dispatcher = self.__in.pop()
            dispatcher.process(self.__handler)
            self.__out.append(dispatcher)

    def __output(self, clients):
        while len(self.__out):
            dispatcher = self.__out.pop()
            try:
                dispatcher.release(self.__names)
            except:
                self.__remove_client(dispatcher.__sock)

    def __remove_client(self, c):
        self.__clients.remove(c)
        c.close()


if __name__ == '__main__':
    params = Params(sys.argv)
    s = Server(params.server_host)
    s.listen()
