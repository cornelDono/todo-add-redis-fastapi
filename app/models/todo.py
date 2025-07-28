from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from utils.static import ToDoStatus


class Todo(BaseModel):
    id: str
    name: str
    status: ToDoStatus
    createdAt: datetime
    updatedAt: datetime
    deletedAt: Optional[datetime] = None
