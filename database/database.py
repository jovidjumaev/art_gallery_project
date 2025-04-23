from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

username = "mnit"
password = "M3ng$run@10"
host = "csdb.fu.campus"
port = 1521
service_name = "CS40"  # match exactly

encoded_password = quote_plus(password)

SQLALCHEMY_DATABASE_URL = (
    f"oracle+oracledb://{username}:{encoded_password}@{host}:{port}/?service_name={service_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
