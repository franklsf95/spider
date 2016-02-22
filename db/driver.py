#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import *
import os

MYSQL_DB_URL = os.getenv('LOCAL_MYSQL')
DATABASE_PATH = '../tmp/db.sqlite3'

Session = sessionmaker()


def prepare_db_session():
    """
    Prepares the database.
    :return: SQLAlchemy session
    """
    # engine = create_engine("sqlite:///{}".format(DATABASE_PATH))
    engine = create_engine(MYSQL_DB_URL)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    Session.configure(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    prepare_db_session()
