from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base


class Position(Base):
    """
    Representing a position in a person's profile
    """
    __tablename__ = 'positions'

    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    title_id = Column(Integer, ForeignKey('titles.id'))
    # company_id = Column(Integer, ForeignKey('companies.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)

    person = relationship('Person', back_populates='positions')
    title = relationship('Title', back_populates='positions')
    # company = relationship('Company', back_populates='position')
