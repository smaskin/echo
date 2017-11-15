class Controller:
    """
    Класс ЧатКонтроллер - класс, обеспечивающий передачу данных из Чата в ГрафическийЧат и обратно;
    обрабатывает события от пользователя (ввод данных, отправка сообщения).
    """
    def __init__(self):
        self.events = []

    def is_empty(self):
        return self.events == []

    def size(self):
        return len(self.events)

    def io(self, event):
        return self.events.append(event)
