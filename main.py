from fastapi import FastAPI
from router.user_routes import user_router
from router.auth_routes import auth_router
from fastapi.middleware.cors import CORSMiddleware
import os


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


# CORS


origins_string = os.getenv("ALLOWED_HOSTS")
origins = origins_string.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers


app.include_router(user_router)
app.include_router(auth_router)
