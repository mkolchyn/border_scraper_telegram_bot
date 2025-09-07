import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

# SQLAlchemy Base
Base = declarative_base()

def get_engine():
    """Create a SQLAlchemy engine."""
    db_url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(db_url, pool_pre_ping=True, future=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
