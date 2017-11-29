import json
import time


def success(text='', code=200, **kwargs):
    msg = {'response': code, 'time': time.time(), **kwargs}
    if text:
        msg['alert'] = text
    return msg


def error(text, code=400):
    return {'response': code, 'time': time.time(), 'error': text}


def unpack(parcel):
    # TODO validate parcel
    return json.loads(parcel.decode())


def pack(dictionary):
    return json.dumps(dictionary).encode()

"""
Поддерживаемые коды ошибок:
    ● 1xx​- информационные сообщения:
        ○ 100​- базовое уведомление;
        ○ 101​- важное уведомление.
    ● 2xx​- успешное завершение:
        ○ 200​- OK;
        ○ 201​(created) - объект создан;
        ○ 202​(accepted)- подтверждение.
    ● 4xx​- ошибка на стороне клиента:
        ○ 400​- неправильный запрос/JSON-объект;
        ○ 401​- не авторизован;
        ○ 402​- неправильный логин/пароль;
        ○ 403​(forbidden) - пользователь заблокирован;
        ○ 404​(not found) - пользователь/чат отсутствует на сервере;
        ○ 409​(conflict) - уже имеется подключение с указанным логином;
        ○ 410​(gone) - адресат существует, но недоступен (offline).
    ● 5xx​- ошибка на стороне сервера:
        ○ 500​- ошибка сервера.
"""

