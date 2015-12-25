#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Person(Base):
    """
    Representing a person of our research interest.
    """
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    headline = Column(String)
    locality = Column(String)
    descriptor = Column(String)
    url = Column(String)
    file_path = Column(String)

    positions = relationship('Position', back_populates='person')
    certifications = relationship('Certification', back_populates='person')
    educations = relationship('Education', back_populates='person')


class Position(Base):
    """
    Representing a position in a person's profile
    """
    __table__ = 'positions'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    title_id = Column(Integer, ForeignKey('titles.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)

    person = relationship('Person', back_populates='positions')
    title = relationship('Title', back_populates='position')
    company = relationship('Company', back_populates='position')
