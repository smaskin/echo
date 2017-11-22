from contact.graphic import Graphic
from contact.list import List


class Controller:
    """
    КонтактКонтроллер - класс, реализующий взаимодействие классов СписокКонтактов и СписокКонтактовGUI;
    """
    def __init__(self, contacts):
        self.list = List(contacts)
        self.gui = Graphic()
