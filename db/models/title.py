from sqlalchemy import Column
from sqlalchemy.orm import relationship
from db.models.base import Base


class Title(Base):
    """
    Representing a title of a job on LinkedIn
    """
    __tablename__ = 'titles'

    name = Column(Base.String)
    url = Column(Base.ShortString, index=True)

    experiences = relationship('PersonExperience', back_populates='title')
