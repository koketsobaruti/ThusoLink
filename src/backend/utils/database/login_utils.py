from sqlalchemy.orm import Session
from src.backend.schemas.user.user_schema import UserLogin
from fastapi import HTTPException, status
from ...models.user.user_model import User
from ...utils.auth.hash_utils import verify_password
from ...models.auth.token_blacklist import TokenBlacklist

from ...utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Login Utils")
class LoginUtils():
    def __init__(self, db: Session):
        self.db = db

    def check_auth(self, user: UserLogin) -> None:
        if user.email == "" or user.password == "":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing email or password."
            )
        
        existing_user = self.db.query(User).filter(User.email == user.email).first()
        
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        logger.info(f"Verifying password for user: {user.email}")
        correct_password = verify_password(user.password, existing_user.password_hash)
        
        if not correct_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return existing_user.id
    
    def get_user_id(self, user) -> int:

        user_db = self.db.query(User).filter(User.email == user.email).first()
        if user_db:
            return user_db.id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
                headers={"WWW-Authenticate": "Bearer"}
            )
    def add_blacklisted_token(self, blacklisted_token: TokenBlacklist) -> None:
        self.db.add(blacklisted_token)
        self.db.commit()