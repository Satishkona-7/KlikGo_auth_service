from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes.auth import router as auth_router
from contextlib import asynccontextmanager

from app.core.database import create_indexes,ping_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ping_database()
    await create_indexes()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Auth Service is running."
    }


@app.get("/health")
async def health():
    return {
        "status": "UP"
    }


app.include_router(
    auth_router,
    prefix=settings.API_PREFIX,
)