from typing import Optional

from pydantic import BaseModel

from models.todo import TodoReddis


class CreateTodoRequestSchema(BaseModel):
    name: str


class CreateTodoResponseSchema(BaseModel):
    pk: str
    name: str

    @classmethod
    def from_entity(cls, to_do: TodoReddis) -> 'CreateTodoResponseSchema':
        return cls(pk=to_do.pk, name=to_do.name)


class CreateNameSpaceRequestSchema(BaseModel):
    name: str

class CreateNameSpaceResponseSchema(BaseModel):
    name: str
    message: Optional[str] = "Successfully created NameSpace"