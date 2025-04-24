from sqlalchemy import Column, CHAR, VARCHAR
from database.database import Base

class Zip(Base):
    __tablename__ = 'ZIP'
    __table_args__ = {'schema': 'JJUMAEV'}  

    zip = Column(CHAR(5), primary_key=True, index=True, nullable=False)
    city = Column(VARCHAR(15), nullable=False)
    state = Column(CHAR(2), nullable=False)
