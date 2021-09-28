from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = None


def create_db_engine(db_conn_string, pool_size=2, max_overflow=0, debug_mode=False):
    return create_engine(
        db_conn_string,
        echo=debug_mode,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_recycle=3600,
        pool_pre_ping=True,
        pool_use_lifo=True,
    )


def create_db_session(engine):
    global Session
    if not Session:
        Session = sessionmaker(bind=engine)
        # todo: setup connection pooling properties
    return Session()


def create_db_schema(engine):
    Base.metadata.create_all(engine)
