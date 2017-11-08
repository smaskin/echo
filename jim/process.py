import message
from config.params import *
from log.dispatcher import Log


def send(sock, msg):
    pack = message.create(msg)
    sock.send(pack)


@Log()
def receive(sock):
    pack = sock.recv(MESSAGE_SIZE)
    return message.decode(pack)
