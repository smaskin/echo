import sys
import socket
from helpers import console
from jim.process import *

if __name__ == '__main__':
    s = socket.socket()
    host = console.host_params(sys.argv, True)
    s.connect(host)
    while True:
        if '-w' in sys.argv:
            message = input('Введите сообщение: ')
            send(s, message)
        response = receive(s)
