from sqlalchemy import Column
from sqlalchemy.orm import relationship
from db.models.base import Base


class Company(Base):
    """
    Representing a company on LinkedIn
    """
    __tablename__ = 'companies'

    name = Column(Base.String)
    url = Column(Base.ShortString, index=True)

    experiences = relationship('PersonExperience', back_populates='company')
