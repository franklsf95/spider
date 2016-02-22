from sqlalchemy import Column
from sqlalchemy.orm import relationship
from db.models.base import Base


class Certification(Base):
    """
    Representing a professional certification on LinkedIn
    """
    __tablename__ = 'certifications'

    name = Column(Base.String)
    url = Column(Base.ShortString, index=True)

    certifications = relationship('PersonCertification', back_populates='certification')
