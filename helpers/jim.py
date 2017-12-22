import json
import time
from config.params import *

DELIMITER = '\n\r'


class Message:
    def __init__(self, **kwargs):
        self.__raw = kwargs
        self.__raw['time'] = time.strftime(DATE_FORMAT)

    def __bytes__(self):
        return '{}{}'.format(json.dumps(self.__raw), DELIMITER).encode()

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
    def user_account_name(self):
        try:
            name = self.__raw['user']['account_name']
        except ValueError:
            return None
        return name

    @property
    def account_name(self):
        try:
            name = self.__raw['account_name']
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
    raw_bytes = socket.recv(MESSAGE_SIZE)

    try:
        raw_string = raw_bytes.decode()
    except UnicodeDecodeError as e:
        return error_request('Got not unicode message {}'.format(e))

    try:
        raw_strings = list(filter(None, raw_string.split(DELIMITER)))
        messages = list(map(json.loads, raw_strings))
    except ValueError as e:
        return error_request('Got not valid json "{}"'.format(raw_string))

    print('Received {}'.format(messages))
    return list(Message(**msg) for msg in messages)


def send(socket, response):
    print('Send {}.'.format(str(response)))
    socket.send(bytes(response))
