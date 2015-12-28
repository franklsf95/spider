from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base


class Education(Base):
    """
    Representing an education entry in a person's profile
    """
    __tablename__ = 'educations'

    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    # school_id = Column(Integer, ForeignKey('schools.id'))
    degree = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)

    person = relationship('Person', back_populates='educations')
    # school = relationship('School', back_populates='educations')
