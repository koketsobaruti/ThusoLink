# app/dependencies.py
from fastapi import Request, HTTPException, status
from ..config.config import settings

def get_current_user(request: Request):
    user = request.session.get("user")  # if using Starlette session middleware
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user
