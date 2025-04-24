from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from database.database import Base

class ShownIn(Base):
    __tablename__ = 'SHOWNIN'
    __table_args__ = {'schema': 'JJUMAEV'}  # Adjust schema as needed

    artworkid = Column(Integer, ForeignKey('JJUMAEV.ARTWORK.artworkid'), primary_key=True, nullable=False)
    showtitle = Column(VARCHAR(50), ForeignKey('JJUMAEV.ARTSHOW.showtitle'), primary_key=True, nullable=False)
