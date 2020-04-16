from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.base import Base


def delete_object(db: Session, obj: Base):
    if not obj:
        raise HTTPException(status_code=404, detail="Object is not found")
    db.delete(obj)
    db.commit()
    return {"status": "OK"}
