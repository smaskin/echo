import json
import time
from config.params import *


class Message:
    def __init__(self, **kwargs):
        self.__raw = kwargs
        self.__raw['time'] = time.strftime(DATE_FORMAT)

    def __bytes__(self):
        return json.dumps(self.__raw).encode()

    def __str__(self):
        return str(self.__raw)

    @property
    def action(self):
        return self.__raw['action'] if 'action' in self.__raw else None

    @property
    def response(self):
        return self.__raw['response'] if 'response' in self.__raw else None

    @property
    def quantity(self):
        return self.__raw['quantity'] if 'quantity' in self.__raw else None

    @property
    def account_name(self):
        try:
            name = self.__raw['user']['account_name']
        except ValueError:
            return None
        return name

    @property
    def msg(self):
        return self.__raw['msg']


def success(response=200, **kwargs):
    return Message(response=response, **kwargs)


def error(text, **kwargs):
    return Message(response=400, error=text, **kwargs)


def error_request(text, **kwargs):
    return Message(action='error', msg=text, **kwargs)


def receive(socket):
    raw_bites = socket.recv(MESSAGE_SIZE)

    try:
        raw_json = raw_bites.decode()
    except UnicodeDecodeError as e:
        return error_request('Got not unicode message {}'.format(e))

    try:
        message = json.loads(raw_json)
    except ValueError as e:
        return error_request('Got not valid json "{}"'.format(raw_json))

    print('Received {}'.format(message))
    return Message(**message)


def send(socket, response):
    print('Send {}.'.format(str(response)))
    socket.send(bytes(response))
