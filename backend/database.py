from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:Chubby%402006@localhost/fintech_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)