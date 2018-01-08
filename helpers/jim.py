import json
import time
from config.params import *
from log.server import server_logger

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
    def user_name(self):
        try:
            name = self.__raw['user_name']
        except ValueError:
            return None
        return name

    @property
    def destination(self):
        return self.__raw['to'] if 'to' in self.__raw else None

    @property
    def sender(self):
        return self.__raw['_from'] if '_from' in self.__raw else None

    @property
    def text(self):
        return self.__raw['text']


def success(response=200, **kwargs):
    return Message(response=response, **kwargs)


def error(text, **kwargs):
    return Message(response=400, error=text, **kwargs)


def error_request(text, **kwargs):
    return Message(action='error', msg=text, **kwargs)


class Dispatcher:
    def __init__(self, client, logger=server_logger):
        self.__sock = client
        self.client_name = None
        self.__logger = logger
        self.__in = []
        self.__out = []

    def receive(self):
        raw_bytes = self.__sock.recv(MESSAGE_SIZE)

        try:
            raw_string = raw_bytes.decode()
        except UnicodeDecodeError as e:
            msg = 'Got not unicode message {}'.format(e)
            self.__logger.info(msg)
            self.__in.append(error_request(msg))
        else:
            try:
                raw_strings = list(filter(None, raw_string.split(DELIMITER)))
                messages = list(map(json.loads, raw_strings))
            except ValueError as e:
                msg = 'Got not valid json "{}"'.format(raw_string)
                self.__logger.info(msg)
                self.__in.append(error_request(msg))
            else:
                self.__logger.info('Received {}'.format(list(messages)))
                self.__in.extend(list(Message(**msg) for msg in messages))
        return self.__in

    def process(self, handler):
        while len(self.__in):
            request = self.__in.pop()
            request.client_name = self.client_name
            response = handler.run_action(request)
            if request.action == 'presence' and response.response == 200:
                self.client_name = request.user_account_name
            if isinstance(response, Message):
                self.__out.append(response)
            else:
                self.__out.extend(response)

    def send(self, request):
        self.__logger.info('Send {}.'.format(str(request)))
        self.__sock.send(bytes(request))

    def release(self, names={}):
        while len(self.__out):
            response = self.__out.pop()
            if response.destination:
                if response.destination in names:
                    client_socket = names[response.destination]
                    self.__logger.info('Send to socket {}: {}.'.format(str(client_socket), str(response)))
                    client_socket.send(bytes(response))
            else:
                self.__logger.info('Send {}.'.format(str(response)))
                self.__sock.send(bytes(response))
