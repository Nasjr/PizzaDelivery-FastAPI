#amsoamso@ Port:5432

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

