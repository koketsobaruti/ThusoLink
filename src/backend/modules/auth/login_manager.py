from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ...utils.database.login_utils import LoginUtils
from src.backend.schemas.user.user_schema import UserLogin
from ...schemas.general_response import GeneralResponse
from ...utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Login Manager")

class LoginManager:
    def __init__(self, db: Session):
        self.db = db
        self.db_utils = LoginUtils(self.db)

    def login_user(self, user:UserLogin) -> GeneralResponse:
        try:
            # Check if the input is valid
            self.db_utils.check_auth(user)
            
            return GeneralResponse(
                status=200,
                message="User logged in successfully"
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