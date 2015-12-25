#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.models import Person, Position

DATABASE_PATH = '../data/db.sqlite3'

Session = sessionmaker()


def prepare_db_session():
    """
    Prepares the database.
    :return: SQLAlchemy session
    """
    engine = create_engine("sqlite:///{}".format(DATABASE_PATH), echo=True)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    Session.configure(bind=engine)
    session = Session()
    return session
