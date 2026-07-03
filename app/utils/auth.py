from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


def create_access_token(data: dict) -> str:
    """
    Creates JWT access token.
    """

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update(
        {
            "exp": expire,
            "iss": settings.JWT_ISSUER,
            "type": "access"
        }
    )

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_access_token(token: str):
    """
    Decode JWT token.
    """

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        issuer=settings.JWT_ISSUER,
    )

    return payload