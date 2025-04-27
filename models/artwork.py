from sqlalchemy import Column, Integer, String, Date, Numeric, CHAR, ForeignKey, Sequence
from database.database import Base

class Artwork(Base):
    __tablename__ = 'ARTWORK'
    __table_args__ = {'schema': 'JJUMAEV'}

    artworkid = Column(
        Integer,
        Sequence('ARTWORKID_SEQUENCE', schema='JJUMAEV'),
        primary_key=True,
        index=True
    )
    artistid = Column(Integer, ForeignKey('JJUMAEV.ARTIST.artistid'), nullable=False)
    worktitle = Column(String(50), nullable=False)
    askingprice = Column(Numeric(8, 2), nullable=True)
    datelisted = Column(Date, nullable=True)
    datereturned = Column(Date, nullable=True)
    dateshown = Column(Date, nullable=True)
    status = Column(String(15), nullable=True)
    workmedium = Column(String(15), nullable=True)
    worksize = Column(String(15), nullable=True)
    workstyle = Column(String(15), nullable=True)
    worktype = Column(String(20), nullable=True)
    workyearcompleted = Column(CHAR(4), nullable=True)
    collectorsocialsecuritynumber = Column(CHAR(9), nullable=True)
