from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///client.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    history = relationship('History', back_populates='contact')

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def __repr__(self):
        return '<Contact ({})>'.format(self.name)


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    message = Column(String)
    contact = relationship('Contact', back_populates='history')

    def __init__(self, contact, message):
        self.contact = contact
        self.message = message

    def __repr__(self):
        return '<History ({}, {})>'.format(self.contact, self.message)


Base.metadata.create_all(engine)
