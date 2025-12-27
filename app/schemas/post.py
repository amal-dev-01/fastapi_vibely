from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    content: str

class PostCreate(BaseModel):
    content: str


class PostUpdate(BaseModel):
    content: str


class PostRead(BaseModel):
    id: str
    user_id: str
    content: str | None
    likes_count: int
    created_at: datetime

    class Config:
        from_attributes = True
