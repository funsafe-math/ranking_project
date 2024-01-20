from sqlalchemy import create_engine, ForeignKey, Column, String, CHAR, Integer, Boolean, Float, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///mydb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)
# Session = sessionmaker(bind=engine)
# session = Session()




