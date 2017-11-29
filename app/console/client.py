from request import Request


class Client:
    @staticmethod
    def get_request():
        text = input('Введите сообщение: ')
        request = Request(action='msg', text=text)
        return bytes(request)

    @staticmethod
    def get_response(parcel):
        return parcel
