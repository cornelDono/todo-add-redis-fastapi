from functools import lru_cache

from punq import Container, Scope
from redis import Redis
from redis.asyncio import Redis

from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()

def _init_container() -> Container:
    container = Container()
    container.register(Config, instance=Config(), scope=Scope.singleton)

    def create_reddis_client() -> Redis:
        return Redis(host=Config().redis_host, port=Config().redis_port, decode_responses=True, db=Config().redis_db)

    container.register(Redis, create_reddis_client, scope=Scope.singleton)

    return container