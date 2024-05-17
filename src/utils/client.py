

from src.exceptions.ip_not_found_exception import IPNotFound


def get_client_ip(request):
    client_ip = request.client.host

    if not client_ip:
        raise IPNotFound

    return client_ip