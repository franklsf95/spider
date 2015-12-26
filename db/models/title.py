from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from db.models.base import Base


class Title(Base):
    """
    Representing a title of a job on LinkedIn
    """
    __tablename__ = 'titles'

    name = Column(String)
    url = Column(String, index=True)

    positions = relationship('Position', back_populates='title')
