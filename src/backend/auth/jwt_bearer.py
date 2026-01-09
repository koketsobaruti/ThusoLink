# app/auth/jwt_bearer.py
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from typing import Optional, List
from ..schemas.token_response import TokenPayload
from ..config.config import settings
from auth.jwt_handler import decode_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)
        # check token expiration
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data.sub
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_active_user(current_user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    # Here you can add additional checks, e.g., if the user is active
    return current_user