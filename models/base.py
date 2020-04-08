from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# TODO: Fix postgres link
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/microblog"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
_Base = declarative_base()


class Base(_Base):
    id = Column(
        Integer, primary_key=True,
        index=True, unique=True
    )
