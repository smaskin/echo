import json
from _socket import socket

import sys

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 7777


def create_message(text):
    json_message = {'text': text}
    return json.dumps(json_message).encode()


def send_message(msg, params=(DEFAULT_IP, DEFAULT_PORT)):
    s = socket()
    s.connect(params)
    s.send(msg)
    reply = b""
    while True:
        piece = s.recv(10)
        reply += piece
        if len(piece) < 10:
            break
    s.close()
    return reply.decode()


def disassemble_message(msg, param):
    return json.loads(msg)[param]


def get_params(argv):
    return argv[1] if len(argv) > 1 else DEFAULT_IP, argv[2] if len(argv) > 2 else DEFAULT_PORT


if __name__ == '__main__':
    message = create_message('Message to the server')
    server_params = get_params(sys.argv)
    response = send_message(message, server_params)
    print(disassemble_message(response, 'status'))
