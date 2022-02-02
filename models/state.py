#!/usr/bin/python3
"""This module contains the State class which inherits from BaseModel"""
from models.base_model import BaseModel, Base
from models.city import City
import models
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """the Sate class
    class attribute:
        __tablename__: name of MySQL table 
        name: string format of state name
        cities: State-City relationship
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='delete')

    if getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def cities(self):
            """returns list of related City instances"""
            list_of_cities = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    list_of_cities.append(city)
            return list_of_cities
