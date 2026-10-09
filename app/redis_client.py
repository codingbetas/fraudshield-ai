import redis

_client = None


def get_redis():
    global _client
    if _client is None:
        _client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True,
        )
    return _client