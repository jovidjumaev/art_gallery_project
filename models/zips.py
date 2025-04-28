from sqlalchemy import Column, CHAR, VARCHAR
from sqlalchemy.orm import relationship
from database.database import Base

class ZIPS(Base):
    __tablename__ = 'ZIPS'
    __table_args__ = {'schema': 'JJUMAEV'}

    zip = Column(CHAR(5), primary_key=True)
    city = Column(VARCHAR(30), nullable=False)
    state = Column(CHAR(2), nullable=False)

    # Relationship to Buyer table
    buyers = relationship("Buyer", back_populates="zip_info") 