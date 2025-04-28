from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression

Base = declarative_base()

class User(Base):
    __tablename__ = "USERS"
    __table_args__ = {'schema': 'JJUMAEV'}

    user_id = Column(Integer, primary_key=True, server_default=text("USER_ID_SEQ.NEXTVAL"))
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
