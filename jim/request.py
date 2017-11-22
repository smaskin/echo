import time

from message import Message
from config.params import *


class Request(Message):
    """
    JSON-данные пересылаемые между клиентом и сервером обязательно должны содержать поля “action” и “time”.
    Поле “action” задаёт тип сообщения между клиентом и сервером.
    Поле “time” - временная метка отправки JSON-объекта, UNIX-время (число секунд от 1 января 1970 года).
    Каждый пользователь при подключении к серверу отсылает сервисное сообщение о присутствии presence с необязательным полем type:
        {
            "action": "presence",
            "time": <unix timestamp>,
            "type": "status",
            "user": {
                "account_name": "C0deMaver1ck",
                "status": "Yep, I am here!"
            }
        }
    Для проверки доступности пользователя online сервер выполняет probe-запрос:
        {
            "action": "probe",
            "time": <unix timestamp>,
        }
    Probe-запрос может отправлять только сервер для проверки доступности клиентов контакт-листа.
    На probe-запрос клиент должен ответить простым presence-сообщением.
    Методы​​протокола​​(actions)
        ● “action”: “presence” - присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online;
        ● “action”: “prоbe” - проверка присутствия. Сервисное сообщение от сервера для проверки присутствии клиента online;
        ● “action”: “msg” - простое сообщение пользователю или в чат;
        ● “action”: “quit” - отключение от сервера;
        ● “action”: “authenticate” - авторизация на сервере;
        ● “action”: “join” - присоединиться к чату;
        ● “action”: “leave” - покинуть чат.
    Протокол может быть расширен новыми методами.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.validate():
            self._raw = {'action': ACTION_PRESENCE}
        self._raw['time'] = time.time()

    def validate(self):
        return 'action' in self._raw and self._raw['action'] in ACTIONS
