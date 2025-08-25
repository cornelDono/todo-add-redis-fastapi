from typing import Set

from redis.asyncio import Redis
from punq import Container
from fastapi import APIRouter, status, Depends, HTTPException

from application.api.routes.namespace.schemas import (
    CreateNameSpaceRequestSchema,
    CreateNameSpaceResponseSchema,
    DeleteNameSpaceRequestSchema,
    DeleteNameSpaceResponseSchema
)
from application.api.schemas import ErrorSchema
from infra.container import init_container
from models.exception import ApplicationException
from models.values.title import Title
from infra.repositories.namespace import RedisNamespaceRepository
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


@router.get(
    "/",
    tags=["namespace"],
    summary="List Namespaces",
    description="Endpoint to get all namespaces",
    status_code=status.HTTP_200_OK,
)
async def list_namespaces(container: Container = Depends(init_container)) -> Set[str]:
    redis_client: Redis = container.resolve(Redis)
    namespaces = await RedisNamespaceRepository(redis_client).get_namespaces()

    return namespaces


@router.post(
    "/{namespace}",
    tags=["namespace"],
    summary="Delete Namespace",
    description="Endpoint to delete namespace"
)
async def delete_namespace(
    schema: DeleteNameSpaceRequestSchema,
    container: Container = Depends(init_container),
) -> DeleteNameSpaceResponseSchema:
    redis_client: Redis = container.resolve(Redis)
    title = Title(value=schema.name.upper())
    is_deleted = await RedisNamespaceRepository(redis_client).delete_namespace(namespace=title.value)

    if not is_deleted:
        message = f"Namespace {title.value} doesnt exist"
        return DeleteNameSpaceResponseSchema(is_deleted=is_deleted, message=message)

    return DeleteNameSpaceResponseSchema(is_deleted=is_deleted)