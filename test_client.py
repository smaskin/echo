# сформировать presence-сообщение;
# отправить сообщение серверу;
# получить ответ сервера;
# разобрать сообщение сервера;
# параметры командной строки скрипта client.py <addr> [<port>]:
#   addr - ip-адрес сервера
#   port - tcp-порт на сервере, по умолчанию 7777

import client

TEXT = 'Test message'


def test_create_message():
    assert client.create_message(TEXT) == b'{"text": "Test message"}'


def test_send_message():
    assert client.send_message(client.create_message(TEXT))


def test_get_request():
    message = b'{"text": "Test message"}'
    assert client.send_message(message) == '{"status": "Ok"}'


def test_disassemble_message():
    assert client.disassemble_message('{"status": "Ok"}', 'status') == 'Ok'


def test_argv():
    assert client.get_params(['client.py']) == ('127.0.0.1', 7777)
    assert client.get_params(['client.py', '192.168.0.1']) == ('192.168.0.1', 7777)
    assert client.get_params(['client.py', '192.168.0.1', 8888]) == ('192.168.0.1', 8888)
