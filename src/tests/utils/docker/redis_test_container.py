from src.tests.utils.docker.container import Container


class RedisTestContainer(Container):
    def __init__(self):
        self.name = "test-redis"

        self.config = {
            "name": self.name,
            "image": "redis:latest",
            "detach": True,
            "ports": {"6379": "6380"},
        }


redis_test_container = RedisTestContainer()
