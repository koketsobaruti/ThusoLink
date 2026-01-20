from fastapi import APIRouter, Request, Depends, HTTPException, status
from ..auth.jwt_bearer import get_current_user
from ..modules.auth.login_manager import LoginManager
from ..schemas.user.user_schema import UserLogin
from ..schemas.general_response import GeneralResponse
from sqlalchemy.orm import Session
from ..database.connection import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from ..models.user.user_model import User
# import logger
import logging
logger = logging.getLogger("thusolink-backend.routes.login")
# import get user from depends folder in dependencies.py
# from backend.config.config import settings
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/logins")
# Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):

    user_login = UserLogin(
        email=form_data.username,  # Swagger sends email as "username"
        password=form_data.password
    )
    logger.info(f"Attempting login for email: {user_login.email}")
    login_manager = LoginManager(db)
    response = login_manager.login_user(user_login)
    logger.info(f"Login response: {response}")
    if response.status != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return response
# @router.post("/login")
# async def login_2(request: Request, user_login: UserLogin, db: Session = Depends(get_db))-> GeneralResponse:
#     # Check credentials (e.g., query DB)
#     login_manager = LoginManager(db)
#     response = login_manager.login_user(user_login)
#     if response.status != 200:
#         return response
#     user = {"username": user_login.email}  # example
#     request.session["user"] = user

#     return response

# Logout
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)):

    login_manager = LoginManager(db)
    login_manager.logout_user(token, current_user.id)
    
        
    return {"message": "Logged out"}

# Protected route
@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "created_at": current_user.created_at
    }
