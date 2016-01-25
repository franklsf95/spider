from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from db.models.base import Base


class Certification(Base):
    """
    Representing a professional certification on LinkedIn
    """
    __tablename__ = 'certifications'

    name = Column(String)
    url = Column(String, index=True)

    certifications = relationship('PersonCertification', back_populates='certification')
