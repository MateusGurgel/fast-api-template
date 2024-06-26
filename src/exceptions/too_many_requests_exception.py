from src.exceptions.http_base_exception.http_exception import HttpException


class TooManyRequestsException(HttpException):
    def __init__(self):
        super().__init__(429, "Too many requests. Please try again later.")
