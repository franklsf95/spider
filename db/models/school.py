from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from db.models.base import Base


class School(Base):
    """
    Representing a school on LinkedIn
    """
    __tablename__ = 'schools'

    name = Column(String)
    url = Column(String, index=True)

    educations = relationship('PersonEducation', back_populates='school')
