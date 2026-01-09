from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ...utils.database.login_utils import LoginUtils
from src.backend.schemas.user.user_schema import UserLogin
from ...schemas.general_response import GeneralResponse
from ...utils.logger_utils import LoggerUtils
from ...schemas.token_response import Token
from ...auth.jwt_handler import create_access_token, create_refresh_token, decode_token
from ...config.config import settings
logger = LoggerUtils.get_logger("Login Manager")

class LoginManager:
    def __init__(self, db: Session):
        self.db = db
        self.db_utils = LoginUtils(self.db)

    def login_user(self, user:UserLogin) -> GeneralResponse:
        try:
            # Check if the input is valid
            self.db_utils.check_auth(user)
            
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(subject=user.email, expires_delta=access_token_expires)
            refresh_token = create_refresh_token(subject=user.email)
            token_response = Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer"
            )
            return GeneralResponse(
                status=200,
                message="User logged in successfully",
                data={"token_response": token_response}
            )
        except HTTPException as e:
            raise  

        except Exception as e:
            logger.error(f"Error during user login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    # def create_session(self, user: dict):
    #     # Logic to create a session for the user
    #     pass

    # def destroy_session(self, request: Request):
    #     # Logic to destroy the user's session
    #     pass

    # def get_current_user(self, request: Request) -> dict:
    #     # Logic to retrieve the current user from the session
    #     pass