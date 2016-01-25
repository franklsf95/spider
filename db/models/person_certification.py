from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base


class PersonCertification(Base):
    """
    Representing a professional certification entry in a person's profile
    """
    __tablename__ = 'person_certifications'

    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    certification_id = Column(Integer, ForeignKey('certifications.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    title = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)

    person = relationship('Person', back_populates='certifications')
    certification = relationship('Certification', back_populates='certifications')
