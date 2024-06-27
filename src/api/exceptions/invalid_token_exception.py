from src.api.exceptions.http_base_exception.http_exception import HttpException


class InvalidTokenException(HttpException):
    def __init__(self):
        super().__init__(401, "Could not validate token")
