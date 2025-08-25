from abc import ABC, abstractmethod
from typing import Set
from dataclasses import dataclass

from redis.asyncio import Redis

from utils.static import NameSpace as NameSpace


@dataclass
class BaseNameSpaceRepository(ABC):
    @abstractmethod
    async def check_namespace_exists(self, namespace: str) -> bool:
        ...

    @abstractmethod
    async def get_namespaces(self) -> Set[str]:
        ...

@dataclass
class BaseRedisRepository(ABC):
    redis_client: Redis


@dataclass
class RedisNamespaceRepository(BaseRedisRepository, BaseNameSpaceRepository):
    async def check_namespace_exists(self, namespace: str) -> bool:
        return bool(await self.redis_client.sismember(NameSpace.Name, namespace))

    async def get_namespaces(self) -> Set[str]:
        namespaces = await self.redis_client.smembers(NameSpace.Name)
        return namespaces

    async def delete_namespace(self, namespace: str) -> bool:
        return bool(await self.redis_client.srem(NameSpace.Name, namespace))