"""Redis Server Connection Settings."""
from typing import Annotated, Generator

from fastapi import Depends
from redis import Redis

from backend.src import config


def get_redis_client() -> Generator[Redis, None, None]:
    redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    try:
        yield redis_client
    finally:
        redis_client.close()

RedisClient = Annotated[Redis, Depends(get_redis_client)]
