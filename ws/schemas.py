from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str

    class Config:
        orm_mode = True
