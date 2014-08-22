#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
All database classes for sqlalchemy ORM.

Every Base class has a Class.q query object. Use for ex. User.q.all() to query
for all users in the database.
"""

from datetime import datetime
from hashlib import sha256
from os import urandom
from random import choice
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
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
    tokens = relationship('FileToken', backref='file')

    def __init__(self, name, user):
        self.name = name
        self.hashstring = self.create_filehash(name)
        self.creation_date = datetime.utcnow()
        self.owner_id = user.id

        # Get the size of the uploaded file
        from sharepy.filehandling import get_filesize_byte
        self.size = get_filesize_byte(user.login, name)

    def __repr__(self):
        return "<File {} ('{}') owned by '{}', created {}>".format(
            self.hashstring, self.name, self.owner.login, self.creation_date)

    def create_filehash(self, filename):
        """Create filehash for storage file (will replace the
        original file name).
        """
        return sha256(filename.encode() + urandom(10)).hexdigest()

    def is_valid(self):
        """Check if a File exists as a file in the storage.
        """
        from sharepy.filehandling import check_storagefile_exist
        return check_storagefile_exist(self.hashstring)


class FileToken(Base):
    """Token which can be shared and used to download files.

    Valid: Bool for enabling/disabling the token
    Downloads max/total: Set a maximum download limit, count the total dls
    """
    __tablename__ = 'filetoken'
    id = Column(Integer, primary_key=True)
    identifier = Column(String, nullable=False, unique=True)
    file_id = Column(Integer, ForeignKey('file.id'), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    valid = Column(Boolean, nullable=False)
    downloads_max = Column(Integer)
    downloads_total = Column(Integer)

    def __init__(self, file_id, downloads_max=0):
        self.identifier = self.create_ident()
        self.file_id = file_id
        self.creation_date = datetime.utcnow()
        self.valid = True
        self.downloads_max = downloads_max
        self.downloads_total = 0

    def __repr__(self):
        return "<FileToken {} for {}>".format(self.identifier, self.file.name)

    def create_ident(self):
        """Create a symbol string as 'name' for the token (used in the link)
        """
        identifier = ''
        for i in range(20):
            identifier += choice('acemnorsuvwxz1234567890')
        return identifier


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
