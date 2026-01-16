from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import uuid
from jose import jwt
from ..config.config import settings
def create_access_token(
    subject: str, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    """
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(),
        "jti": str(uuid.uuid4()),  # ✅ Add unique token ID
        "token_type": "access"
        # "roles": roles
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    """
    Create JWT refresh token
    """
    expire = datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(),
        "jti": str(uuid.uuid4()),
        "token_type": "refresh"
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode JWT token
    """
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return decoded_token