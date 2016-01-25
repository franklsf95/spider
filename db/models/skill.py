from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from db.models.base import Base


class Skill(Base):
    """
    Representing a professional skill on LinkedIn
    """
    __tablename__ = 'skills'

    name = Column(String)
    url = Column(String, index=True)

    skills = relationship('PersonSkill', back_populates='skill')
