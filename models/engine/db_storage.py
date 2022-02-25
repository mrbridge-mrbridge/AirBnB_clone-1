#!/usr/bin/python3
"""module is also a storage for abstraction purpose
   using MySQL
"""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

classes = {"Amenity": Amenity, 
           "BaseModel": BaseModel,
           "City": City,
           "Place": Place,
           "Review": Review,
           "State": State,
           "User": User}


class DBStorage:
    """the DBStotage Class"""
    
    __engine = None
    __session = None

    def __init__(self):
        """class instantiation"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadat.drop_all(self.__engine)

    def all(self, cls=None):
        """returns dict of cls if it exists, else return dict of everything"""
        dem_all = {}
        if cls is not None:
            for item in self.__session.query(cls).all():
                key = item.__class__.__name__ + '.' + item.id
                dem_all[key] = item
        else:
            for obj in classes.values():
                for item in self.__session.query(obj).all():
                    key = item.__class__.__name__ + '.' + item.id
                    dem_all[key] = item
        return dem_all

    def new(self, obj):
        """add new object to database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes made to database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj (if not None) from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables and sessions"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """"calls the remove() method of sqlalchemy"""
        self.__session.remove()
