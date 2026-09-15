import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Database Configuration (MySQL with SQLite local fallback)
MYSQL_USER = os.getenv("DB_USER", "root")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "")
MYSQL_HOST = os.getenv("DB_HOST", "localhost")
MYSQL_PORT = os.getenv("DB_PORT", "3306")
MYSQL_DB = os.getenv("DB_NAME", "vms_db")

MYSQL_URL = (
    f"mysql+pymysql://{quote_plus(MYSQL_USER)}:{quote_plus(MYSQL_PASSWORD)}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)
SQLITE_URL = "sqlite:///./vms_db.db"

# Try connecting to MySQL; fallback to SQLite if MySQL is unavailable locally
try:
    engine = create_engine(MYSQL_URL, pool_pre_ping=True)
    # Test connection
    with engine.connect() as conn:
        pass
    print("Successfully connected to MySQL database.")
except Exception as e:
    print(f"MySQL connection warning ({e}). Falling back to SQLite local database.")
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
