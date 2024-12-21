from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# Database URL
db_url = "mysql+pymysql://myuser:mypassword@db:3306/user_management"
engine = create_engine(db_url)

Base = declarative_base()

# Retry mechanism for database connection
def initialize_database():
    retries = 5
    for i in range(retries):
        try:
            with engine.connect() as connection:
                print("Connected to the database!")
                break
        except Exception as e:
            print(f"Attempt {i + 1} failed: {e}")
            time.sleep(5)
    else:
        raise Exception("Failed to connect to the database after multiple retries.")

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for myapi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
