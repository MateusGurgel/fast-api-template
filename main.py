import os
import uvicorn
from fastapi import FastAPI
from src.middlewares.error_handler import error_handler_middleware
from src.exceptions.http_base_exception.http_exception import HttpException
from src.exceptions.http_base_exception.http_exception_handler import http_exception_handler
from src.modules.user.user_router import user_router
from src.modules.authentication.authentication_router import auth_router
from fastapi.middleware.cors import CORSMiddleware
from src.middlewares.rate_limit import rate_limit_middleware
from starlette.middleware.base import BaseHTTPMiddleware

description = """
## My FastAPI Template
"""

app = FastAPI(
    title="FastAPI Template",
    description=description,
    summary="That is my favorite template.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
)


# Including Erro Handlers

app.add_exception_handler(HttpException, http_exception_handler)

# Including middlewares

cors_origins_string = os.getenv("ALLOWED_HOSTS")
cors_origins = cors_origins_string.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)


# Including routers

app.include_router(user_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)