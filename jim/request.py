import time
import json


class Request:
    def __init__(self, **kwargs):
        self._raw = kwargs
        self._raw['time'] = time.time()

    def __bytes__(self):
        return json.dumps(self._raw).encode()
