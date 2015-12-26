from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from db.models.base import Base


class Person(Base):
    """
    Representing a person of our research interest.
    """
    __tablename__ = 'people'

    name = Column(String)
    headline = Column(String)
    locality = Column(String)
    meta = Column(String)

    positions = relationship('Position', back_populates='person')
    # certifications = relationship('Certification', back_populates='person')
    # educations = relationship('Education', back_populates='person')