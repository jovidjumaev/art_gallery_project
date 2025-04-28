from sqlalchemy import Column, Integer, Numeric, CHAR, VARCHAR, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Buyer(Base):
    __tablename__ = 'BUYER'
    __table_args__ = {'schema': 'JJUMAEV'}  

    buyerid = Column(Integer, Sequence('BUYERID_SEQUENCE', schema='JJUMAEV'), primary_key=True)
    firstname = Column(VARCHAR(15), nullable=False)
    lastname = Column(VARCHAR(20), nullable=False)
    street = Column(VARCHAR(50), nullable=True)
    zip = Column(CHAR(5), ForeignKey('JJUMAEV.ZIPS.zip'), nullable=True)
    areacode = Column(CHAR(3), nullable=True)
    telephonenumber = Column(CHAR(7), nullable=True)
    purchaseslastyear = Column(Numeric(8, 2), nullable=True)
    purchasesyeartodate = Column(Numeric(8, 2), nullable=True)

    # Relationship to ZIPS table
    zip_info = relationship("ZIPS", back_populates="buyers")
