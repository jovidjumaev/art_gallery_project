from sqlalchemy import Column, Integer, Sequence, String, Date, ForeignKey, CHAR
from database.database import Base

potential_customer_id_seq = Sequence('POTENTIALCUSTOMERID_SEQUENCE', schema='JJUMAEV')

class PotentialCustomer(Base):
    __tablename__ = "POTENTIALCUSTOMER"
    __table_args__ = {'schema': 'JJUMAEV'}  # <--- Add this line!

    potentialcustomerid = Column(Integer, potential_customer_id_seq, primary_key=True, server_default=potential_customer_id_seq.next_value())
    firstname = Column(String(15), nullable=False)
    firstname = Column(String(15), nullable=False)
    lastname = Column(String(20), nullable=False)
    areacode = Column(CHAR(3))
    telephonenumber = Column(CHAR(7))
    street = Column(String(50))
    zip = Column(CHAR(5))
    datefilledin = Column(Date)
    preferredartistid = Column(Integer)  # FK to Artist(artistid)
    preferredmedium = Column(String(15))
    preferredstyle = Column(String(15))
    preferredtype = Column(String(20))
