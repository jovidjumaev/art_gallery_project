from sqlalchemy import Column, Integer, Numeric, Date, CHAR, ForeignKey
from database.database import Base

class Sale(Base):
    __tablename__ = 'SALE'  # Corrected table name
    __table_args__ = {'schema': 'JJUMAEV'}  # Schema for Oracle

    invoicenumber = Column(Integer, primary_key=True, index=True)
    artworkid = Column(Integer, ForeignKey('JJUMAEV.ARTWORK.artworkid'), nullable=False)
    amountremittedtoowner = Column(Numeric(8, 2), nullable=True, default=0.00)
    saledate = Column(Date, nullable=True)
    saleprice = Column(Numeric(8, 2), nullable=True)
    saletax = Column(Numeric(6, 2), nullable=True)
    buyerid = Column(Integer, ForeignKey('JJUMAEV.COLLECTOR.collectorid'), nullable=False)
    salespersonssn = Column(CHAR(9), nullable=True)
