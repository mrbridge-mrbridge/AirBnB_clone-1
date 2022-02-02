#!/usr/bin/python3
"""This module contains the City class which inherits from BaseModel"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """the City class
    class attribute:
        state_id: string format of state.id
        name: string format of city name
    """
    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
