# app/auth/jwt_bearer.py
from datetime import datetime
from click import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from typing import Optional, List
from ..schemas.token_response import TokenPayload
from ..config.config import settings
from .jwt_handler import decode_token
from ..models.user.user_model import User
from ..database.connection import get_db
from sqlalchemy.orm import Session
from ..models.auth.token_blacklist import TokenBlacklist

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/logins/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> TokenPayload:
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
         # ✅ Check if token is blacklisted
        jti = payload.get("jti")
        if jti:
            is_blacklisted = db.query(TokenBlacklist).filter(
                TokenBlacklist.jti == jti
            ).first()
            
            if is_blacklisted:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked. Please login again.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        # check type of token
        user_id = UUID(token_data.sub)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_active_user(current_user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    # Here you can add additional checks, e.g., if the user is active
    return current_user