# - принимает сообщение клиента;
# - формирует ответ клиенту;
# - отправляет ответ клиенту;
# - имеет параметры командной строки:
#   -p <port> - TCP-порт для работы (по умолчанию использует порт 7777)
#   -a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)

import server
from socket import *

TEXT = 'Test message'


class TestServer:
    __client = None

    def setup(self):
        s = socket()
        self.__client = server.get_client(s, ['server.py'])

    def test_receive_message(self):
        assert server.receive_message(self.__client) == {'text': TEXT}

    def test_create_response(self):
        request = server.receive_message(self.__client)
        assert server.create_response(request) == {'status': 'Ok'}

    def test_send_response(self):
        response = {'status': 'Ok'}
        assert server.send_response(self.__client, response)

    def test_argv(self):
        assert server.get_params(['server.py']) == (server.DEFAULT_IP, server.DEFAULT_PORT)
        assert server.get_params(['server.py', '192.168.0.1']) == ('192.168.0.1', server.DEFAULT_PORT)
        assert server.get_params(['server.py', '192.168.0.1', 8888]) == ('192.168.0.1', 8888)
