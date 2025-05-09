import sqlmodel
from sqlmodel import SQLModel, Session
from .config import DATABASE_URL

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
        yield session

def init_db():
    print("creating database")
    SQLModel.metadata.create_all(get_engine())