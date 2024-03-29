#!/usr/bin/python3
""" User class """
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ class User that inherits from BaseModel """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship("Place", cascade="all, delete-orphan",
                          backref="user")
    reviews = relationship("Review", cascade="all, delete-orphan",
                           backref='user')
