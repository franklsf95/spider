from sqlalchemy import Column
from sqlalchemy.orm import relationship
from db.models.base import Base


class School(Base):
    """
    Representing a school on LinkedIn
    """
    __tablename__ = 'schools'

    name = Column(Base.String)
    url = Column(Base.ShortString, index=True)

    educations = relationship('PersonEducation', back_populates='school')
