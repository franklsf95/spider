from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from db.models.base import Base


class Company(Base):
    """
    Representing a company on LinkedIn
    """
    __tablename__ = 'companies'

    name = Column(String)
    url = Column(String, index=True)

    experiences = relationship('PersonExperience', back_populates='company')
