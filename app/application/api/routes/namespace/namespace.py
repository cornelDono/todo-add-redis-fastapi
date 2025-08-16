from redis.asyncio import Redis
from punq import Container
from fastapi import APIRouter, status, Depends, HTTPException

from application.api.routes.namespace.schemas import CreateNameSpaceRequestSchema, CreateNameSpaceResponseSchema
from application.api.schemas import ErrorSchema
from infra.container import init_container
from models.exception import ApplicationException
from models.values.title import Title
from utils.static import NameSpace

router = APIRouter()


@router.post(
    "/",
    tags=["namespace"],
    summary="Create NameSpace",
    description="Endpoint for new namespace creation",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': CreateNameSpaceResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_namespace(
        schema: CreateNameSpaceRequestSchema,
        container: Container = Depends(init_container),
) -> CreateNameSpaceResponseSchema:
    redis_client: Redis = container.resolve(Redis)
    title = Title(value=schema.name)

    try:
        namespace = await redis_client.sadd(NameSpace.Name, title.value.upper())
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    if not namespace:
        message = f"Namespace {title.value.upper()} already exists"
        return CreateNameSpaceResponseSchema(name=title.value.upper(), message=message)

    return CreateNameSpaceResponseSchema(name=title.value.upper())
