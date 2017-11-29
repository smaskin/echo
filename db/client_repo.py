from sqlalchemy import func
from db.client import session, Contact


class ClientRepo:
    def __init__(self):
        self._session = session

    def get_contacts(self):
        return self._session.query(func.count(Contact.id)).scalar()
