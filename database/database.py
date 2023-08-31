from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

metadata_obj = MetaData()
Base = declarative_base()

engine = create_engine("sqlite+pysqlite:///requests.db")
conn = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()



