"""Optional Redis transport placeholder."""


class RedisTransport:
    def __init__(self, redis_url: str) -> None:
        self.redis_url = redis_url

    async def publish(self, payload: dict) -> None:
        raise NotImplementedError("Redis transport is not implemented yet")
