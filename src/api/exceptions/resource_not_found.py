from src.api.exceptions.http_base_exception.http_exception import HttpException


class ResourceNotFound(HttpException):
    def __init__(self):
        super().__init__(404, "resource not found")
