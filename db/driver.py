#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.models import Person

Session = sessionmaker()


def main():
    engine = create_engine('sqlite:///../data/test.db', echo=True)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    Session.configure(bind=engine)
    session = Session()

    p = Person(name='Frank')
    session.add(p)
    session.commit()


if __name__ == '__main__':
    main()
