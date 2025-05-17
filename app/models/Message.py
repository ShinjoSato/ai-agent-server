from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    message: str
    language: str
    type: int # 0: トーク, 1: 設定
    status: int # -1: error, 0: proceed, 1: end 
    # created_at: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="messages")
