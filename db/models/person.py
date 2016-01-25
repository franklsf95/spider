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

    experiences = relationship('PersonExperience', back_populates='person')
    certifications = relationship('PersonCertification', back_populates='person')
    educations = relationship('PersonEducation', back_populates='person')
