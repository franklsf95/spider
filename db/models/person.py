from sqlalchemy import Column
from sqlalchemy.orm import relationship
from db.models.base import Base


class Person(Base):
    """
    Representing a person of our research interest.
    """
    __tablename__ = 'people'

    name = Column(Base.String)
    headline = Column(Base.String)
    locality = Column(Base.String)
    meta = Column(Base.String)

    experiences = relationship('PersonExperience', back_populates='person')
    educations = relationship('PersonEducation', back_populates='person')
    certifications = relationship('PersonCertification', back_populates='person')
    skills = relationship('PersonSkill', back_populates='person')
