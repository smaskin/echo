from message import Message


class Response(Message):
    """
    Класс JIMОтвет - класс, реализующий ответ (response) по протоколу JIM.
        Ответы сервера должны содержать поле “response”, а также могут содержать поле “alert”/“error” с текстом ошибки.
        В случае, если какое-то действие требует авторизации, сервер должен ответить соответствующим кодом ошибки 401.
        После подключения при необходимости авторизации клиент должен отправить сообщение авторизации c логином/паролем, например:
            {
                "action": "authenticate",
                "time": <unix timestamp>,
                "user": {
                    "account_name": "C0deMaver1ck",
                    "password": "CorrectHorseBatteryStaple"
                }
            }
        В ответ сервер может прислать один из кодов:
            {
                "response": 200,
                "alert":"Необязательное сообщение/уведомление"
            }
            {
                "response": 402,
                "error": "This could be "wrong password" or "no account with that name""
            }
            {
                "response": 409,
                "error": "Someone is already connected with the given user name"
            }
        Отключение от сервера должно сопровождаться сообщением “quit”:
            {
                "action": "quit"
            }
        Коды​​ответов​​сервера
            JIM-протокол использует коды ошибок HTTP (они уже многим знакомы).
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
            Коды ошибок могут быть дополнены новыми кодами.
        Сообщения-ответы имеют следующий формат (в зависимости от кода ответа):
            {
                "response": 1xx / 2xx,
                "time": <unix timestamp>,
                "alert": "message (optional for 2xx codes)"
            }
            или
            {
                "response": 4xx / 5xx,
                "time": <unix timestamp>,
                "error": "error message (optional)"
            }
    """
    def __init__(self, parcel, **kwargs):
        super().__init__(**kwargs)
        self.__parcel = parcel
        self._raw['response'] = 200
