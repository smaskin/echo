from message import Message


class Response(object):
    """
    Класс JIMОтвет - класс, реализующий ответ (response) по протоколу JIM.
    """
    def __init__(self, request):
        self.__request = request

    def pack(self):
        msg = Message('Ответ сервера на сообщение - ' + self.__request.text)
        return msg.pack()
