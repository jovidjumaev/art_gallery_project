from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
import os
import getpass

username = os.getenv("DB_USERNAME")
password = getpass.getpass(prompt="Enter your database password: ")
host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT"))
service_name = os.getenv("DB_SERVICE_NAME")

encoded_password = quote_plus(password)

SQLALCHEMY_DATABASE_URL = (
    f"oracle+oracledb://{username}:{encoded_password}@{host}:{port}/?service_name={service_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
