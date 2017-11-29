import time
import message
from db.server_repo import ServerRepo


class Response:
    def __init__(self, parcel):
        print('Запрос "{}".'.format(parcel))
        self.__parcel = message.unpack(parcel)
        self.__response = self.__generate()

    def __bytes__(self):
        return message.pack(self.__response)

    @property
    def code(self):
        return self.__response['response']

    def __generate(self):
        if type(self.__parcel) is dict and 'action' in self.__parcel:
            controller = self.__get_controller()
            if self.__parcel['action'] not in dir(controller):
                result = message.error('Action is not available')
            else:
                result = controller.run_action()
        else:
            result = message.error('Action is invalid')
        return result

    def __get_controller(self):
        # TODO router for different controllers depending on action
        return Controller(self.__parcel)


class BaseController:
    def __init__(self, parcel):
        self._parcel = parcel
        self._repo = ServerRepo()

    def run_action(self):
        if self.__time_validate():
            return getattr(self, self._parcel['action'])()
        else:
            return message.error('Time is invalid')

    def __time_validate(self):
        return 'time' in self._parcel and self._parcel['time'] < time.time()


class Controller(BaseController):
    def presence(self):
        return message.success()

    def msg(self):
        return message.success()

    def get_contacts(self):
        count = self._repo.get_contacts()
        return message.success(quantity=count)

    def contact_list(self):
        pass

    def add_contact(self):
        pass

    def del_contact(self):
        pass
