import json
import time
from config.params import *


class Message(object):
    """
    Класс JIMСообщение - класс, реализующий сообщение (msg) по протоколу JIM.
    """
    def __init__(self, text='', type=MESSAGE_TYPE_DEFAULT, status=MESSAGE_STATUS_OK, when=time.time()):
        self.__msg = {'type': type, 'status': status, 'message': text, 'time': when}

    @property
    def dict(self):
        return self.__msg

    def pack(self):
        return json.dumps(self.__msg).encode()
