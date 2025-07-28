from datetime import datetime
from uuid import uuid4

from redis import Redis
from punq import Container
from fastapi import APIRouter, status, Depends

from infra.container import init_container
from models.todo import Todo
from utils.static import ToDoStatus

router = APIRouter()

@router.get(
    "",
    tags=["todo"],
    summary="Get todo",
    response_description="",
    status_code=status.HTTP_200_OK,
    response_model=Todo,
)
def get_todo(
    container: Container = Depends(init_container)
) -> Todo:
    redis_client: Redis = container.resolve(Redis)

    return Todo(
        name="first_todo",
        id=uuid4().hex,
        status=ToDoStatus.ToDo,
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )