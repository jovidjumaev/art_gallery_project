from sqlalchemy import Column, Integer, Numeric, Date, CHAR, ForeignKey, Sequence
from sqlalchemy.schema import FetchedValue
from database.database import Base

class Sale(Base):
    __tablename__ = 'SALE'
    __table_args__ = {'schema': 'JJUMAEV'}

    invoicenumber = Column(
        Integer, 
        Sequence('SALE_INVOICE_SEQUENCE', schema='JJUMAEV'),
        primary_key=True,
        server_default=FetchedValue()
    )
    
    artworkid = Column(Integer, ForeignKey('JJUMAEV.ARTWORK.artworkid'))
    amountremittedtoowner = Column(Numeric(10, 2))
    saledate = Column(Date)
    saleprice = Column(Numeric(10, 2))
    saletax = Column(Numeric(6, 2))
    buyerid = Column(Integer, ForeignKey('JJUMAEV.BUYER.buyerid'))
    salespersonssn = Column(CHAR(9), ForeignKey('JJUMAEV.SALESPERSON.socialsecuritynumber'))
