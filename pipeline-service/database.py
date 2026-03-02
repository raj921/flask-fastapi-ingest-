import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/customer_db")
engine = create_engine(url, connect_args={"connect_timeout": 5})
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
