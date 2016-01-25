from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base


class PersonSkill(Base):
    """
    Representing a professional certification entry in a person's profile
    """
    __tablename__ = 'person_skills'

    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'))

    person = relationship('Person', back_populates='skills')
    skill = relationship('Skill', back_populates='skills')
