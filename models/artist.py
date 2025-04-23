from sqlalchemy import Column, Integer, String, Date, Numeric, CHAR
from database.database import Base

class Artist(Base):
    __tablename__ = 'ARTIST'  # Make sure this matches the exact name in Oracle
    __table_args__ = {'schema': 'JJUMAEV'}  # Reference your partner's schema

    artistid = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(15), nullable=False)
    lastname = Column(String(20), nullable=False)
    interviewdate = Column(Date, nullable=True)
    interviewername = Column(String(35), nullable=True)
    areacode = Column(CHAR(3), nullable=True)
    telephonenumber = Column(CHAR(7), nullable=True)
    street = Column(String(50), nullable=True)
    zip = Column(CHAR(5), nullable=True)
    saleslastyear = Column(Numeric(8, 2), nullable=True)
    salesyeartodate = Column(Numeric(8, 2), nullable=True)
    socialsecuritynumber = Column(CHAR(9), nullable=True)
    usualmedium = Column(String(15), nullable=True)
    usualstyle = Column(String(15), nullable=True)
    usualtype = Column(String(20), nullable=True)
