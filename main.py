import uvicorn
from fastapi import FastAPI
from src.modules.user.user_router import user_router
from src.modules.authentication.authentication_router import auth_router
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)