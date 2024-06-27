from fastapi import Request
from fastapi.responses import JSONResponse

from src.api.exceptions.http_base_exception.http_exception import HttpException


async def http_exception_handler(request: Request, exc: HttpException):
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.body},
    )
