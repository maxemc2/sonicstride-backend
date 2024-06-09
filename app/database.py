from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Local Application Imports
from config import setting

# Format the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{setting.database_user}:{setting.database_password}"
    f"@{setting.database_url}:5432/{setting.database_name}"
)

# Create a SQLAlchemy engine instance which provides a source of connectivity to our database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a factory for SQLAlchemy session instances that are bound to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the declarative base model that other models will inherit from
# This is a class that includes directives to describe the actual database table it will be mapped to
Base = declarative_base()