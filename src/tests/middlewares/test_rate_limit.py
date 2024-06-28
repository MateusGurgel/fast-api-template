from decouple import config


def test_rate_limit(client):

    requests_per_time = config("RATE_LIMIT_REQUESTS_PER_RESET_TIME", cast=int)
    for i in range(requests_per_time):
        response = client.get("users/me")
        assert response.status_code == 401

    response = client.get("users/me")
    assert response.status_code == 429
