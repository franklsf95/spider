import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

print(sqlalchemy.__version__)

Base = declarative_base()


class Person(Base):
    """
    Representing a person of our research interest.
    """
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_name = Column(String)
    url = Column(String)

    def __repr__(self):
        return "<Person '{}', url='{}'>".format(self.name, self.url)

print(Person.__table__)

if __name__ == '__main__':
    db = create_engine('sqlite:///test.db', echo=True)
    Base.metadata.create_all(db)
