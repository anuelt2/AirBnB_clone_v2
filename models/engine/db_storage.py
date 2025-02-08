#!/usr/bin/python3
"""Database Storage Engine"""
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Define the Database Storage Engine"""

    __engine = None

    __session = None

    def __init__(self):
        mysql_user = os.getenv("HBNB_MYSQL_USER")
        mysql_pwd = os.getenv("HBNB_MYSQL_PWD")
        mysql_host = os.getenv("HBNB_MYSQL_HOST")
        mysql_db = os.getenv("HBNB_MYSQL_DB")

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(mysql_user,
                                                      mysql_pwd,
                                                      mysql_host,
                                                      mysql_db
                                                      )
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name argument cls"""
        obj_dict = {}
        if cls:
            models = [cls]
        else:
            models = [User, State, City, Amenity, Place, Review]
        for model in models:
            rows = self.__session.query(model).all()
            for row in rows:
                key = f"{type(row).__name__}.{row.id}"
                obj_dict.update({key: row})
        return obj_dict

    def new(self, obj):
        """Add the obj to the current database session(self.__session)"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        # inspector = inspect(self.__engine)  # new line 1
        # existing_tables = inspector.get_table_names()  # new line 2

        # for table in Base.metadata.tables.values():
        #    if table.name in existing_tables:
        #        table.create(self.__engine, checkfirst=True)

        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """Closes database connections after each request"""
        self.__session.remove()
