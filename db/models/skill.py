from sqlalchemy import Column
from sqlalchemy.orm import relationship
from db.models.base import Base


class Skill(Base):
    """
    Representing a professional skill on LinkedIn
    """
    __tablename__ = 'skills'

    name = Column(Base.String)
    url = Column(Base.ShortString, index=True)

    skills = relationship('PersonSkill', back_populates='skill')
