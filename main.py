from fastapi import FastAPI
from router.user_routes import user_router
from router.auth_routes import auth_router
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

# CORS

origins_string = os.getenv("ALLOWED_HOSTS")
origins = origins_string.split(",")
app.add_middleware(CORSMiddleware(origins))

# Include routers

app.include_router(user_router)
app.include_router(auth_router)
