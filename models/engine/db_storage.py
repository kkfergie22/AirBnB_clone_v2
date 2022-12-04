#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship


class DBstorage:
    """This class manages storage of hbnb models in JSON format

    Attributes:
        __engine (sqlalchemy.engine.base.Engine): database engine
        __session (sqlalchemy.orm.session.Session): database session
    """

    __engine = None
    __session = None

    def __init__(self):
        """This class manages storage of hbnb models in JSON format"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            return {k: v for k, v in self.__objects.items()
                    if k.split('.')[0] == cls.__name__}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__session.add(obj)

    def save(self):
        """Saves storage dictionary to file"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Reloads the database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """calls remove() method on the private session attribute"""
        self.__session.close()
