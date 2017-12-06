from sqlalchemy import func
from db.server import session, Client


class ServerRepo:
    def __init__(self):
        self.__session = session

    def get_contacts(self):
        return self.__session.query(func.count(Client.id)).scalar()

    def add_client(self, account_name):
        client = Client(account_name)
        self.__session.add(client)
        return self.__session.commit()

    def get_contact_list(self):
        return self.__session.query(Client).all()
