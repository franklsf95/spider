from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base


class PersonExperience(Base):
    """
    Representing a position in a person's profile
    """
    __tablename__ = 'person_experiences'

    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    title_id = Column(Integer, ForeignKey('titles.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)

    person = relationship('Person', back_populates='experiences')
    title = relationship('Title', back_populates='experiences')
    company = relationship('Company', back_populates='experiences')
