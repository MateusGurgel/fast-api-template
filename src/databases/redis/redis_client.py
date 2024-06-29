from decouple import config
from redis import Redis


class RedisClient:

    def __init__(self):
        self.client = Redis(
            host=config("REDIS_HOST"),
            port=config("REDIS_PORT", cast=int),
            decode_responses=True,
        )

    def set_client(self, host=config("REDIS_HOST"), port=config("REDIS_PORT")):
        """
        Set the Redis client
        """
        client = Redis(
            host=host,
            port=port,
            decode_responses=True,
        )

        self.client = client

    def get_client(self) -> Redis:
        """
        Get the Redis client
        """
        return self.client

    def get(self, key):
        """
        Get the value stored in Redis for the given key.

        :param key: The key for which the value needs to be retrieved from Redis.
        :return: The value stored in Redis for the given key.
        """
        return self.client.get(key)

    def set(self, key, value: str, ex: int = 3600):
        """
        :param key: the key to set in the Redis database
        :param value: the value to set for the given key
        :param ex: the expiration time in seconds for the key-value pair (default is 3600 seconds)
        :return: None

        Set the given key-value pair in the Redis database with an optional expiration time.
        If the ex parameter is not provided, the key-value pair will expire after 3600 seconds by default.
        """
        self.client.set(key, value, ex)

    def delete(self, key):
        """
        Delete a key-value pair from Redis.

        :param key: The key to delete.
        :return: None.
        """
        self.client.delete(key)

    def flushdb(self):
        self.client.flushdb()


redis_client = RedisClient()
