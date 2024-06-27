from fastapi import Request
from src.api.exceptions.http_base_exception.http_exception import HttpException
from src.api.exceptions.http_base_exception.http_exception_handler import (
    http_exception_handler,
)


async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HttpException as e:
        response = await http_exception_handler(request, e)
        return response
