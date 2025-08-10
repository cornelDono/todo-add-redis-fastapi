from datetime import datetime
from typing import Optional

from aredis_om import HashModel, Field

from utils.static import ToDoStatus


class TodoReddis(HashModel):
    name: str
    status: ToDoStatus = Field(default=ToDoStatus.ToDo)
    createdAt: datetime = Field(default=datetime.now())
    updatedAt: datetime = Field(default=datetime.now())
    deletedAt: Optional[datetime] = Field(default=None)