
"""
module: base.py
This module contains the base class for the cache service
"""
import redis


def get_redis_client(redis_url):
    """
    This function returns a redis client object
    param: redis_url: str
    """
    return redis.Redis.from_url(redis_url, decode_responses=True)
    
        