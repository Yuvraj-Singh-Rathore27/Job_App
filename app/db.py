import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# ENV variable will tell if we are running tests or production
ENV = os.getenv("ENV", "prod")

if ENV == "test":
    # SQLite DB for GitHub Actions CI
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # Your original PostgreSQL DB
    DATABASE_URL = "postgresql://postgres:12345@localhost:5432/job_app"
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError as e:
        print("❌ Database connection failed:", e)
        return False
