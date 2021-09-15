from dotenv import load_dotenv

load_dotenv('../.env')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine(os.environ.get("SQLALCHEMY_DATABASE_URI"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
postgre_db = scoped_session(SessionLocal)
Base.query = postgre_db.query_property()
