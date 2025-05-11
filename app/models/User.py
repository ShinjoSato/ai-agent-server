from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: int # 0: bot, 1: user
    name: str
    voice_url: Optional[str]

    messages: List["Message"] = Relationship(back_populates="user")
