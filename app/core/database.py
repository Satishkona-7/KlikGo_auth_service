from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from typing import AsyncGenerator
from app.core.config import settings


async def get_database() -> AsyncGenerator:
    yield database

    
client = AsyncIOMotorClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]

async def ping_database():
    await client.admin.command("ping")

async def create_indexes():
    await database["users"].create_index(
        [("email", ASCENDING)],
        unique=True
    )


def get_database():
    return database