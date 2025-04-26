from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.task import PriorityEnum, StatusEnum

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=3)
    due_date: datetime
    priority: PriorityEnum
    status: StatusEnum

    model_config = ConfigDict(arbitrary_types_allowed=True)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=3)
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class TaskResponse(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
