from jose import JWTError
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError
from app.core.config import settings

from app.core.database import get_database
from app.core.exceptions import (
    UnauthorizedException,
    TokenExpiredException,
    InvalidTokenException,
)   
from app.models.user_model import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import AuthService
from app.utils.auth import decode_access_token
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

security = HTTPBearer()


def get_auth_service(
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    return AuthService(db)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=201,
)
async def signup(
    user: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    return await service.signup(user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    user: UserLogin,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(user)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service),
):

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")
        issuer = payload.get("iss")
        token_type = payload.get("type")

        if not user_id:
            raise UnauthorizedException()

        if issuer != settings.JWT_ISSUER:
            raise InvalidTokenException()

        if token_type != "access":
            raise InvalidTokenException()

    except ExpiredSignatureError:

        raise TokenExpiredException()

    except JWTError:

        raise InvalidTokenException()

    return await service.get_user_by_id(user_id)