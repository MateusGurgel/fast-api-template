from src.exceptions.http_base_exception.http_exception import HttpException


class IPNotFound(HttpException):
    def __init__(self):
        super().__init__(400, "Could not find you ip address")
