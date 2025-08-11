from datetime import datetime
from uuid import uuid4

from redis import Redis
from punq import Container
from fastapi import APIRouter, status, Depends, HTTPException

from application.api.routes.schemas import CreateTodoRequestSchema, CreateTodoResponseSchema, \
    CreateNameSpaceRequestSchema, CreateNameSpaceResponseSchema
from application.api.schemas import ErrorSchema
from infra.container import init_container
from models.exception import ApplicationException
from models.todo import TodoReddis
from models.values.title import Title

router = APIRouter()


@router.post(
    "/",
    tags=["todo"],
    summary="Get todo",
    description="Endpoint for new todo creation",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': CreateTodoResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_todo(
    schema: CreateTodoRequestSchema,
    container: Container = Depends(init_container),
) -> CreateTodoResponseSchema:
    redis_client: Redis = container.resolve(Redis)

    title = Title(value=schema.name)
    to_do = TodoReddis(name=title.value)

    try:
        to_do_object = await to_do.save()
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateTodoResponseSchema.from_entity(to_do_object)
