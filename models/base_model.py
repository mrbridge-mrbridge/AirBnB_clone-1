#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from uuid import uuid4
from datetime import datetime
import models, os


class BaseModel:
    """A base class for all hbnb models"""
    id = ''
    created_at = ''
    updated_at = ''

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model
        args: not used
        kwargs: attributes as 'id','created_at','updated_at'
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not kwargs:
            models.storage.new(self)
        else:
            for k, v in kwargs.items():
                if k in ['created_at', 'updated_at']:
                    self.__dict__[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[k] = v

            """kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)"""

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
