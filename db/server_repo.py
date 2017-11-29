from sqlalchemy import func
from db.server import session, Client


class ServerRepo:
    def __init__(self):
        self._session = session

    def get_contacts(self):
        return self._session.query(func.count(Client.id)).scalar()
