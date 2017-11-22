class List:
    """
    СписокКонтактов - класс, реализующий операции с контактами (добавление, удаление);
    """
    def __init__(self, contacts):
        self.contacts = contacts

    def add(self, contact):
        self.contacts.append(contact)

    def remove(self, contact):
        self.contacts.remove(contact)
