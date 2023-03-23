import redis
from app.core.config import setting


def create_pool():
    return redis.ConnectionPool.from_url(url=setting.redis_uri, decode_responses=True)


pool = create_pool()
