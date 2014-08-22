#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Database connection related code.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Workaround to enforce foreign key constraints in sqlite3.
    See https://www.sqlite.org/foreignkeys.html and
    http://docs.sqlalchemy.org/en/rel_0_9/dialects/sqlite.html
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def database_init(_remove=False):
    """Initialize the database and remove the old one if needed.
    Also the place for example data to be commited after setup.
    """
    if _remove:
        print('Removing current database file.')
        from os import remove
        remove('sharepy.db')

    print('Initialize database.')
    from sharepy.database import File, User, Role, FileToken
    Base.metadata.create_all(bind=engine)

    # Example data
    session.add(Role('administration'))
    session.add(User('admin', 'John Doe', 'admin', None, 1))
    session.commit()


engine = create_engine('sqlite:///sharepy.db', echo=False)
session = scoped_session(sessionmaker(engine,
                                      autocommit=False,
                                      autoflush=False))
Base = declarative_base()
Base.q = session.query_property()



