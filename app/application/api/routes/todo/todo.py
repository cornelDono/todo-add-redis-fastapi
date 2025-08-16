from redis.asyncio import Redis
from aredis_om import NotFoundError
from punq import Container
from fastapi import APIRouter, status, Depends, HTTPException

from application.api.routes.todo.schemas import CreateTodoResponseSchema, CreateTodoRequestSchema
from application.api.schemas import ErrorSchema
from infra.container import init_container
from models.exception import ApplicationException
from models.todo import TodoReddis
from models.values.title import Title

router = APIRouter(tags=["todo"])


@router.get(
    "/{todo_pk}/",
    summary="Get todo by ID",
    description="Endpoint ot get ToDo by ID",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': TodoReddis},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def get_todo(
    todo_pk: str,
    container: Container = Depends(init_container),
) -> TodoReddis:
    redis_client: Redis = container.resolve(Redis)

    try:
        todo = await TodoReddis.get(todo_pk)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Todo with ID {} not found'.format(todo_pk)})
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return todo


@router.post(
    "/",
    summary="Create todo",
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
