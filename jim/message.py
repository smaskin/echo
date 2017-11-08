import json
import time
from config.params import *


def create(msg, type=MESSAGE_TYPE_DEFAULT, status=MESSAGE_STATUS_OK, when=time.time()):
    message = {
        'type': type,
        'status': status,
        'message': msg,
        'time': when
    }
    return encode(message)


def encode(msg):
    return json.dumps(msg).encode()


def decode(msg):
    return json.loads(msg.decode())
