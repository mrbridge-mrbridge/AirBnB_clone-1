#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import ForeignKey, Column, String, Integer, Float
import models
from os import getenv
from models.review import Review
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) == "db":
        self.reviews = relationship("Review", backref="place", cascade="delete")
    else:
        @property
        def reviews(self):
            """Get a list of all linked Reviews."""
            review_list = []
            for rev in list(models.storage.all(Review).values()):
                if rev.place_id == self.id:
                    review_list.append(rev)
            return review_list
