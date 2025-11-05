from sqlalchemy.orm import Session
from src.backend.schemas.user.user_schema import UserLogin
from fastapi import HTTPException, status
from ...models.user.user_model import User
from backend.utils.auth.hash_utils import verify_password
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
                detail="Invalid email or password."
            )
        
        logger.info(f"Verifying password for user: {user.email}")
        correct_password = verify_password(user.password, existing_user.password_hash)
        
        if not correct_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password."
            )
        
        return None