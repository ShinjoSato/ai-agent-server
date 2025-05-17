from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: int # 0: brain, 1: voice, 2: emotion

    messages: List["Message"] = Relationship(back_populates="role")
