import sys
import socket
import select
from helpers import console
from jim.process import *


def read_requests(r_clients, all_clients):
    responses = {}
    for c in r_clients:
        try:
            responses[c] = receive(c)
        except:
            print('Клиент {} {} отключился'.format(c.fileno(), c.getpeername()))
            all_clients.remove(c)

    return responses


def write_responses(requests, w_clients, all_clients):
    for sender in requests:
        for c in w_clients:
            try:
                response = requests[sender]
                response['type'] = MESSAGE_TYPE_REQUEST
                send(c, response)
            except:
                print('Клиент {} {} отключился.'.format(c.fileno(), c.getpeername()))
                c.close()
                all_clients.remove(c)


if __name__ == '__main__':
    server = socket.socket()
    host = console.host_params(sys.argv)
    server.bind(host)
    server.listen(WORKERS)
    server.settimeout(0.2)
    clients = []
    while True:
        try:
            client, address = server.accept()
        except OSError as e:
            pass
        else:
            print('Получен запрос на соединение от {}'.format(address))
            clients.append(client)
        finally:
            read = []
            write = []
            try:
                read, write, e = select.select(clients, clients, [], 0)
            except Exception as e:
                print('Исключение при опросе клиентов - {}'.format(e.args))

            requests = read_requests(read, clients)
            write_responses(requests, write, clients)
