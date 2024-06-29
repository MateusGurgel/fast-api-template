import time

from docker import DockerClient, from_env
from docker.errors import NotFound


class Container:
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config

    def stop(self):
        client = from_env()
        container_name = self.name

        try:
            existing_container = client.containers.get(container_name)
            print(f"Removing existing {container_name} container")
            existing_container.stop()
            existing_container.remove()
            print("Existing container removed")
        except NotFound:
            print("Test Container not found")

    def start(self) -> DockerClient:
        client = from_env()

        self.stop()

        container = client.containers.run(**self.config)

        while not self.is_ready(container):
            time.sleep(1)

        if not self.wait_for_stable_status(container):
            raise RuntimeError("Container did not stabilize within the specified time")

        return container

    def is_ready(self, container: DockerClient) -> bool:
        container.reload()
        return container.status == "running"

    def wait_for_stable_status(
        self, container: DockerClient, stable_duration=4, interval=1
    ):
        start_time = time.time()
        stable_count = 0

        while time.time() - start_time < stable_duration:
            if self.is_ready(container):
                stable_count += 1
            else:
                stable_count = 0

            if stable_count == stable_duration / interval:
                return True

            time.sleep(interval)

        return False
