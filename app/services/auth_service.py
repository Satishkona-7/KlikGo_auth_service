from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

from app.core.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.models.user_model import (
    TokenResponse,
    UserCreate,
    UserInDB,
    UserLogin,
    UserResponse,
)
from app.utils.auth import create_access_token
from app.utils.password import hash_password, verify_password


class AuthService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def signup(self, user: UserCreate) -> UserResponse:

        # MongoDB unique index handles duplicate emails.

        now = datetime.now(timezone.utc)

        new_user = {
            "name": user.name,
            "email": user.email,
            "password": hash_password(user.password),
            "role": "customer",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }

        try:

            result = await self.collection.insert_one(new_user)

        except DuplicateKeyError:

            raise UserAlreadyExistsException()

        return UserResponse(
            id=str(result.inserted_id),
            name=user.name,
            email=user.email,
            role="customer",
        )

    async def login(self, user: UserLogin) -> TokenResponse:

        db_user = await self.collection.find_one(
            {"email": user.email}
        )

        if not db_user:
            raise InvalidCredentialsException()

        if not verify_password(
            user.password,
            db_user["password"],
        ):
            raise InvalidCredentialsException()

        token = create_access_token(
            {
                "sub": str(db_user["_id"]),
                "email": db_user["email"],
                "role": db_user["role"],
            }
        )

        return TokenResponse(
            access_token=token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def get_user_by_id(
        self,
        user_id: str,
    ) -> UserResponse:

        if not ObjectId.is_valid(user_id):
            raise UserNotFoundException()

        user = await self.collection.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

        if not user:
            raise UserNotFoundException()

        return UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            role=user["role"],
        )

    async def get_user_by_email(
        self,
        email: str,
    ) -> UserInDB | None:

        user = await self.collection.find_one(
            {
                "email": email
            }
        )

        if not user:
            return None

        return UserInDB(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            password=user["password"],
            role=user["role"],
            is_active=user["is_active"],
            created_at=user["created_at"],
            updated_at=user["updated_at"],
        )

    async def delete_all_users(self):
        """
        Useful during testing.
        """
        await self.collection.delete_many({})