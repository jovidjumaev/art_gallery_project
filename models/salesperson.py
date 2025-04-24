from sqlalchemy import Column, CHAR, VARCHAR
from database.database import Base

class Salesperson(Base):
    __tablename__ = 'SALESPERSON'
    __table_args__ = {'schema': 'JJUMAEV'}  # Adjust schema as needed

    socialsecuritynumber = Column(CHAR(9), primary_key=True, index=True)
    firstname = Column(VARCHAR(15), nullable=False)
    lastname = Column(VARCHAR(20), nullable=False)
    street = Column(VARCHAR(50), nullable=True)
    zip = Column(CHAR(5), nullable=True)
