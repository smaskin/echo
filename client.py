import sys
import socket
import jim
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


class Client:
    def __init__(self, name):
        self.__name = name
        self.__sock = socket.socket()

    def connect(self, address, status='Yep, I am here!'):
        self.__sock.connect(address)
        request = jim.Message(action='presence', type='status', user={'account_name': self.__name, 'status': status})
        jim.send(self.__sock, request)
        return jim.receive(self.__sock)

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
            reply = jim.receive(self.__sock)
            if reply.response == 202 and reply.quantity > 0:
                # TODO receive sub responses
                response_items = []
                for i in range(reply.quantity):
                    response_items.append(reply(socket))


    def close(self):
        self.__sock.close()


if __name__ == '__main__':
    console_params = Params(sys.argv)
    client = Client(console_params.account_name)
    client.connect(console_params.console_host)
    client.emit()
