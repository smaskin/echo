import json
from message import Message


class Request(object):
    def __init__(self, request):
        self.__raw = request

    @property
    def dict(self):
        try:
            msg = json.loads(self.__raw.decode())
        except ValueError:
            msg = Message(self.__raw).dict
        return msg

    @property
    def text(self):
        return self.dict['message'] if 'message' in self.dict else 'Nothing'
