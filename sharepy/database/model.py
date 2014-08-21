#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
All database classes for sqlalchemy ORM.

Every Base class has a Class.q query object. Use for ex. User.q.all() to query
for all users in the database.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from utils import hash_password, verify_password


class User(Base):
    """A user class with common fields.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    name = Column(String)
    password = Column(String, nullable=False)
    email = Column(String, unique=True)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    files = relationship('File', backref='owner')

    def __init__(self, login, name, password, email, role_id):
        self.login = login
        self.name = name
        self.password = hash_password(password)
        self.email = email
        self.role_id = role_id

        # If the user is created, create his upload dir
        from sharepy.filehandling import create_useruploaddir
        create_useruploaddir(login)

    def __repr__(self):
        return "<User '{}'>".format(self.login)

    def verify_password(self, password):
        return verify_password(password, self.password)

    def is_authenticated(self):
        """Needed for flask-login"""
        return True

    def is_active(self):
        """Needed for flask-login"""
        return True

    def is_anonymous(self):
        """Needed for flask-login"""
        return False

    def get_id(self):
        """Needed for flask-login"""
        return self.id


class File(Base):
    """A file in the storage, identified by its hash. Has one owner.
    """
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hashstring = Column(String, nullable=False, unique=True)
    creation_date = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, name, owner_id):
        self.name = name
        self.creation_date = datetime.utcnow()
        self.owner_id = owner_id

        # Create a hash as name for the new storage file
        from sharepy.filehandling import create_filehash
        self.hashstring = create_filehash(name)

        # Get the size of the uploaded file
        from sharepy.filehandling import get_filesize_byte
        self.size = get_filesize_byte(User.q.get(owner_id).login, name)

    def __repr__(self):
        return "<File {} ('{}') owned by '{}', created {}>".format(
            self.hashstring, self.name, User.q.get(self.owner_id).login,
            self.creation_date)


class Role(Base):
    """Roles that can be used for a permission system.
    """
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    members = relationship('User', backref='role')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role '{}'>".format(self.name)
