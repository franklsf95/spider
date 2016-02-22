from sqlalchemy import Column, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base


class PersonEducation(Base):
    """
    Representing an education entry in a person's profile
    """
    __tablename__ = 'person_educations'

    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    school_id = Column(Integer, ForeignKey('schools.id'))
    degree = Column(Base.String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)

    person = relationship('Person', back_populates='educations')
    school = relationship('School', back_populates='educations')
