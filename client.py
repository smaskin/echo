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


def interact():
    print('\n'.join(['{}. {}'.format(key, action['name']) for key, action in enumerate(ACTIONS, 1)]))
    try:
        num = abs(int(input('Выберите действие или введите сообщение: ')))
    except ValueError:
        num = 0
    config = ACTIONS[num - 1] if num <= len(ACTIONS) else ACTIONS[0]
    params = {'action': config['action']}
    if 'params' in config:
        for param in config['params']:
            p = str(input('Выберите параметр "{}": '.format(param)))
            params[param] = p
    return jim.Message(**params)


class Handler:
    def __init__(self, sock, input_):
        self._sock = sock
        self._input = input_
        self.is_alive = False

    def __call__(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            self.run()

    def stop(self):
        self.is_alive = False

    def run(self):
        pass


class Receiver(Handler):
    def run(self):
        messages = jim.receive(self._sock)
        while len(messages):
            msg = messages.pop()
            self._input.put(msg)


class ConsoleOutput(Handler):
    def run(self):
        request = self._input.get()
        if request.action == 'contact_list':
            print(request.account_name)


class Client:
    def __init__(self, name):
        self.__name = name
        self.__sock = socket.socket()
        input_ = Queue()

        listener = Receiver(self.__sock, input_)
        self.__listen_thread = Thread(target=listener)
        self.__listen_thread.daemon = True

        handler = ConsoleOutput(self.__sock, input_)
        self.__handler_thread = Thread(target=handler)
        self.__handler_thread.daemon = True

    def connect(self, address, status='Yep, I am here!'):
        self.__sock.connect(address)
        request = jim.Message(action='presence', type='status', user={'account_name': self.__name, 'status': status})
        jim.send(self.__sock, request)
        if jim.receive(self.__sock):
            self.__listen_thread.start()
            self.__handler_thread.start()
            return True
        else:
            return False

    def emit(self):
        while True:
            message = interact()
            jim.send(self.__sock, message)

    def close(self):
        self.__listen_thread.is_alive = False
        self.__handler_thread.is_alive = False
        self.__sock.close()


if __name__ == '__main__':
    console_params = Params(sys.argv)
    client = Client(console_params.account_name)
    if client.connect(console_params.console_host):
        client.emit()
