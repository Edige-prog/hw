from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, WebSocket, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/login")

SECRET_KEY = "TOP_SECRET111"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

class CookieOrHeaderTokenScheme(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str:
        # First try to get token from the authorization header
        try:
            token = await super().__call__(request)
            if token:
                return token
        except HTTPException:
            # If no valid auth header, check cookies
            token = request.cookies.get("access_token")
            if token:
                return token
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Create the scheme instance
oauth2_scheme = CookieOrHeaderTokenScheme(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    """Hash the user's password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the hashed password matches the plain password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(user_id: int) -> str:
    """Create a JWT token for the given user ID."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(user_id),  # Ensure user_id is converted to string
        "exp": expire.timestamp()  # Add expiration as timestamp
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str) -> int:
    """Decode the JWT token and extract the user ID."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format - missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            return int(user_id_str)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format - user ID not valid",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )