from contact.list import List


class Graphic:
    """
    СписокКонтактовGUI - базовый класс для отображения списка контактов (консольный, графический, WEB)
    """
    def __init__(self, contacts):
        self.list = List(contacts)

    def show(self, type):
        pass
