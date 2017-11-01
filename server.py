import json
import sys
from getopt import getopt
from socket import *

DEFAULT_IP = '0.0.0.0'
DEFAULT_PORT = 7777
WORKERS = 1


def get_client(sock, argv):
    sock.bind(get_params(argv))
    sock.listen(WORKERS)
    worker, address = sock.accept()
    return worker


def receive_message(sock):
    message = b""
    while True:
        piece = sock.recv(10)
        message += piece
        if len(piece) < 10:
            break
    return message.decode()


def create_response(status):
    message = {'status': 'Ok' if status else 'Failure'}
    return json.dumps(message).encode()


def send_response(sock, msg):
    return sock.send(msg)


def get_params(argv):
    optlist, args = getopt(argv[1:], 'a:p:')
    ip = DEFAULT_IP
    port = DEFAULT_PORT
    for opt, arg in optlist:
        if opt == '-a':
            ip = arg
        elif opt == '-p':
            port = arg
    return ip, port


if __name__ == '__main__':
    s = socket()
    client = get_client(s, sys.argv)
    request = receive_message(client)
    response = create_response(True)
    print('Ok' if send_response(client, response) else 'Failure')
    s.close()

