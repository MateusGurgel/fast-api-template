
from src.exceptions.http_base_exception.http_exception import HttpException
class credentialsException(HttpException):
    def __init__(self):
        super().__init__(401, "Could not validate credentials")