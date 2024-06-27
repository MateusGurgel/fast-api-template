from src.api.exceptions.http_base_exception.http_exception import HttpException


class EmailAlreadyUsedException(HttpException):
    def __init__(self):
        super().__init__(409, "Email already in use.")
