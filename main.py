from decouple import config, Csv
import uvicorn
from fastapi import FastAPI
from src.api.middlewares.error_handler import error_handler_middleware
from src.api.exceptions.http_base_exception.http_exception import HttpException
from src.api.exceptions.http_base_exception.http_exception_handler import http_exception_handler
from src.api.modules.user.user_router import user_router
from src.api.modules.authentication.authentication_router import auth_router
from fastapi.middleware.cors import CORSMiddleware
from src.api.middlewares.rate_limiter import rate_limiter_middleware
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
    openapi_url=config("DOCS_URL"),
)

# Including Erro Handlers

app.add_exception_handler(HttpException, http_exception_handler)

# Including middlewares
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limiter_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)


# Including routers

app.include_router(user_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)