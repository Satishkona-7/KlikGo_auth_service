from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists."
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized."
        )


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

class TokenExpiredException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=401,
            detail="Token has expired."
        )


class InvalidTokenException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=401,
            detail="Invalid token."
        )