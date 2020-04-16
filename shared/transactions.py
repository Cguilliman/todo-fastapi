from contextlib import contextmanager
from sqlalchemy.orm import Session


@contextmanager
def atomic(db: Session):
    """Simple transaction implementation in context manager"""
    try:
        db.begin_nested()
        yield
    except Exception as e:
        db.rollback()
        raise e
    finally:
        pass


def atomic_decorator(func):
    def wrapped(db: Session, *args, **kwargs):
        with atomic(db):
            return func(db, *args, **kwargs)
    return wrapped
