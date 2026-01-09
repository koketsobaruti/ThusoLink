from fastapi import APIRouter, Request, Depends, HTTPException, status
from ..depends.dependencies import get_current_user
from ..modules.auth.login_manager import LoginManager
from ..schemas.user.user_schema import UserLogin
from ..schemas.general_response import GeneralResponse
from sqlalchemy.orm import Session
from ..database.connection import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
# import get user from depends folder in dependencies.py
# from backend.config.config import settings
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
# Login
@router.post("/login")
# async def login(form_data: UserLogin, db: Session = Depends(get_db)) -> GeneralResponse:
#     login_manager = LoginManager(db)
#     result = login_manager.login_user(form_data)
#     if result.status != 200:
#         raise HTTPException(status_code=result.status, detail=getattr(result, "detail", "Invalid credentials"))
#     return result
async def login(request: Request, user_login: UserLogin, db: Session = Depends(get_db))-> GeneralResponse:
    # Check credentials (e.g., query DB)
    login_manager = LoginManager(db)
    response = login_manager.login_user(user_login)
    if response.status != 200:
        return response
    user = {"username": user_login.email}  # example
    request.session["user"] = user

    return response

# Logout
@router.post("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return {"message": "Logged out"}

# Protected route
@router.get("/me")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user
