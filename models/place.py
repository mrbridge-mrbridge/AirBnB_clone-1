#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import ForeignKey, Column, String, Integer, Float
import models
from os import getenv
from models.review import Review
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from models.amenity import Amenity
from models.review import Review


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                                      primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'),
                                        primary_key=True, nullable=False))


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
        reviews = relationship("Review", backref="place", cascade="delete")
        amenities = relationship('Amenity', secondary='place_amenity',
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """Get a list of all linked Reviews."""
            review_list = []
            for rev in list(models.storage.all(Review).values()):
                if rev.place_id == self.id:
                    review_list.append(rev)
            return review_list
        @property
        def amenities(self):
            """returns the list of Amenity instances based on criteria"""
            amenity_list = []
            for item in list(models.storage.all(Amenity).values()):
                if item.id in self.amenity_ids:
                    amenity_list.append(item)
            return amenity_list
        @amenities.setter
        def amenities(self, obj):
            """adding an Amenity.id to the attribute amenity_ids"""
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
