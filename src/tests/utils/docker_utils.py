import time

import docker


def stop_test_database_container():
    client = docker.from_env()
    container_name = "test-database"

    try:
        existing_container = client.containers.get(container_name)
        print(f"Removing existing {container_name} container")
        existing_container.stop()
        existing_container.remove()
        print("Existing container removed")
    except docker.errors.NotFound:
        print("Test Container not found")


def is_container_ready(container: docker.DockerClient) -> bool:
    container.reload()
    return container.status == "running"


def wait_for_stable_status(
    container: docker.DockerClient, stable_duration=3, interval=1
):
    start_time = time.time()
    stable_count = 0

    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
        else:
            stable_count = 0

        if stable_count == stable_duration / interval:
            return True

        time.sleep(interval)

    return False


def start_test_database_container() -> docker.DockerClient:
    client = docker.from_env()
    container_name = "test-database"

    stop_test_database_container()

    container_config = {
        "name": container_name,
        "image": "postgres:latest",
        "detach": True,
        "ports": {"5432": "5435"},
        "environment": {
            "POSTGRES_DB": "test_db",
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_password",
        },
    }

    container = client.containers.run(**container_config)

    while not is_container_ready(container):
        time.sleep(1)

    if not wait_for_stable_status(container):
        raise RuntimeError("Container did not stabilize within the specified time")

    return container
