# src/backend/database/connection.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config.config import Settings

# Load settings
settings = Settings()
DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing in your config settings.")

# SQLAlchemy engine setup
engine = create_engine(DATABASE_URL)

# Test connection
def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT NOW();"))
            print("Current Time:", result.fetchone()[0])
        print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect to DB: {e}")


# Session configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
