from src.tests.utils.docker.container import Container


class PostgresTestContainer(Container):
    def __init__(self):
        self.name = "test-database"

        self.config = {
            "name": self.name,
            "image": "postgres:latest",
            "detach": True,
            "ports": {"5432": "5435"},
            "environment": {
                "POSTGRES_DB": "test_db",
                "POSTGRES_USER": "test_user",
                "POSTGRES_PASSWORD": "test_password",
            },
        }

        super().__init__(self.name, self.config)


postgree_test_container = PostgresTestContainer()
