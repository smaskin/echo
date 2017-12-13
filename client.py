import jim
import sys
import socket
from threading import Thread
from queue import Queue
from console import Params

ACTIONS = (
    {
        'action': 'msg',
        'name': 'Послать сообщение',
        'params': ('text',)
    },
    {
        'action': 'get_contacts',
        'name': 'Список контактов',
    },
    {
        'action': 'quit',
        'name': 'Выйти'
    }
)


class Receiver:
    def __init__(self, sock, responses):
        self.__sock = sock
        self.__responses = responses
        self.is_alive = False

    def __call__(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            reply = jim.receive(self.__sock)
            if reply:
                self.__responses.put(reply)
            else:
                break

    def stop(self):
        self.is_alive = False


class Client:
    def __init__(self, name):
        self.__name = name
        self.__sock = socket.socket()
        self.__responses = Queue()

        listener = Receiver(self.__sock, self.__responses)
        self.__listen_thread = Thread(target=listener)
        self.__listen_thread.daemon = True

    def connect(self, address, status='Yep, I am here!'):
        self.__sock.connect(address)
        request = jim.Message(action='presence', type='status', user={'account_name': self.__name, 'status': status})
        jim.send(self.__sock, request)
        if jim.receive(self.__sock):
            self.__listen_thread.start()
            return True
        else:
            return False

    def emit(self):
        while True:
            print('\n'.join(['{}. {}'.format(key, action['name']) for key, action in enumerate(ACTIONS, 1)]))
            try:
                num = int(input('Выберите действие: '))
            except ValueError:
                continue

            try:
                config = ACTIONS[num - 1]
            except IndexError:
                continue

            params = {'action': config['action']}
            if 'params' in config:
                for param in config['params']:
                    p = str(input('Выберите параметр "{}": '.format(param)))
                    params[param] = p

            msg = jim.Message(**params)
            jim.send(self.__sock, msg)

    def close(self):
        self.__listen_thread.is_alive = False
        self.__sock.close()


if __name__ == '__main__':
    console_params = Params(sys.argv)
    client = Client(console_params.account_name)
    if client.connect(console_params.console_host):
        client.emit()
