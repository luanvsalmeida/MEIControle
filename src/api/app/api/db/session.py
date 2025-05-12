import sqlmodel
from sqlmodel import SQLModel, Session
from .config import DATABASE_URL, DB_TIMEZONE
import timescaledb
from sqlalchemy import text

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = sqlmodel.create_engine(DATABASE_URL)
    return _engine



def get_session():
    engine = get_engine()
    with Session(engine) as session:
        session.exec(text(f"SET TIME ZONE '{DB_TIMEZONE}'"))
        yield session

def init_db():
    print("creating database")
    SQLModel.metadata.create_all(get_engine())
    #print("creating hypertables")
    #timescaledb.metadata.create_all(get_engine())