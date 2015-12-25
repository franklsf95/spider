import db_declarative
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def main():
    db = create_engine('sqlite:///test.db', echo=True)
    Base.metadata.create_all(db)


if __name__ == '__main__':
    main()
