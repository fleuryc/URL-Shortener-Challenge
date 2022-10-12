"""Database package

Defines SQLAlchemy entities :
- engine : the database query engine based on the connexion string
- session : the database connexion for this session
- base : the database declarative mapping
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

# get settings from Pydantic Settings
settings = dict(get_settings())
SQLALCHEMY_DATABASE_URL = settings["SQLALCHEMY_DATABASE_URL"]

# create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# create the connexion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create the mapping
Base = declarative_base()
