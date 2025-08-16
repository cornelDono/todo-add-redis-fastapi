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