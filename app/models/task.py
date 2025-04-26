from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from app.models.enum import PriorityEnum, StatusEnum

if TYPE_CHECKING:
    from app.models.user import User  

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    priority: PriorityEnum
    status: StatusEnum
    due_date: datetime
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")  

    owner: Optional["User"] = Relationship(back_populates="tasks")
