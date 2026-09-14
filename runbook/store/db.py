from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

def get_engine(url: str):
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)

def get_sessionmaker(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db(engine):
    Base.metadata.create_all(bind=engine)
