from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.utils.settings import settings

Base = declarative_base()   #Connects models with actual db


# engine = create_engine(url=settings.DB_CONNECTION)

engine = create_engine(
    settings.DB_CONNECTION,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=10,
    max_overflow=20,
)


LocalSession = sessionmaker(bind=engine)


def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
