#!/usr/bin/python3
""" Amenity module """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Amenity class that inherits from BaseModel """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
