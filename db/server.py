"""
В качестве опорной схемы базы данных предлагается следующий вариант.
На стороне сервера БД содержит следующие таблицы:
    -клиент:
        логин;
        информация.
    -историяклиента:
        время входа;
        ip-адрес.
    -списокконтактов (составляется на основании выборки всех записей с id_владельца)
        id_владельца;
        id_клиента.
"""
import time
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///server.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

contact_table = Table('contact', Base.metadata,
                      Column('client_id', Integer, ForeignKey('client.id')),
                      Column('contact_id', Integer, ForeignKey('client.id'))
                      )


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    history = relationship('History', back_populates='client')
    contacts = relationship('Client', secondary=contact_table,
                            backref='owner',
                            primaryjoin=id == contact_table.c.client_id,
                            secondaryjoin=id == contact_table.c.contact_id
                            )

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def __repr__(self):
        return '<Client ({})>'.format(self.name)


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    ip = Column(String)
    timestamp = Column(String)
    client = relationship('Client', back_populates='history')

    def __init__(self, client, ip):
        self.ip = ip
        self.client = client
        self.timestamp = time.time()

    def __repr__(self):
        return '<History ({})>'.format(self.ip)


Base.metadata.create_all(engine)
