import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
db_url = "mysql+pymysql://myuser:mypassword@db:3306/user_management"
engine = create_engine(db_url)

# Retry mechanism to connect to the database
retries = 5
for i in range(retries):
    try:
        with engine.connect() as connection:
            print("Connected to the database!")
            break
    except Exception as e:
        print(f"Attempt {i + 1} failed: {e}")
        time.sleep(5)  # Wait for 5 seconds before retrying
else:
    raise Exception("Failed to connect to the database after multiple retries.")

Base = declarative_base()

# Create all tables
Base.metadata.create_all(bind=engine)

# Session and Base setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)