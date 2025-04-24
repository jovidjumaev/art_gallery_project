from sqlalchemy import Column, Integer, Date, VARCHAR
from database.database import Base

class ArtShow(Base):
    __tablename__ = 'ARTSHOW'
    __table_args__ = {'schema': 'JJUMAEV'} 

    showtitle = Column(VARCHAR(50), primary_key=True, index=True, nullable=False)
    showfeaturedartistid = Column(Integer, nullable=True)
    showclosingdate = Column(Date, nullable=True)
    showtheme = Column(VARCHAR(50), nullable=True)
    showopeningdate = Column(Date, nullable=True)
