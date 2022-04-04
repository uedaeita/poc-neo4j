from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings

engine = create_engine(
    Settings.SQLALCHEMY_DATABASE_URI,
    # pool_size=10,
    # max_overflow=2,
    # pool_recycle=300,
    # pool_pre_ping=True,
    # pool_use_lifo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
