from datetime import datetime, timezone, timedelta
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
from ...models.auth.token_blacklist import TokenBlacklist

class LoginManager:
    def __init__(self, db: Session):
        self.db = db
        self.db_utils = LoginUtils(self.db)

    def login_user(self, user:UserLogin) -> GeneralResponse:
        try:
            
            # Check if the input is valid and return the user ID if it is
            user_id = self.db_utils.check_auth(user)
            if not user_id:
                logger.warning(f"Failed login attempt for email: {user.email}")
            logger.info(f"User ID {user_id} authenticated successfully.")
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(subject=user_id, expires_delta=access_token_expires)
            refresh_token = create_refresh_token(subject=user_id)
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
    def logout_user(self, token: str) -> GeneralResponse:
        try:
            payload = decode_token(token)
            jti = payload.get("jti")
            user_id = payload.get("sub")
            token_type = payload.get("token_type")
            expires_at = payload.get("exp")
            if not jti or not user_id or not token_type or not expires_at:
                logger.warning("Invalid token data during logout.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token data"
                )
            expires_datetime = datetime.fromtimestamp(expires_at, tz=timezone.utc)
            
            blacklisted_token = TokenBlacklist(
                jti=jti,
                user_id=user_id,
                token_type=token_type,
                expires_at=expires_datetime
            )
            self.db_utils.add_blacklisted_token(blacklisted_token)
            logger.info(f"Token with JTI {jti} blacklisted successfully for user {user_id}.")
            return GeneralResponse(
                status=200,
                message="User logged out successfully"
            )
        except HTTPException as e:
            raise  
        except Exception as e:
            logger.error(f"Error during user logout: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Logout error: {str(e)}"
            )

    # def destroy_session(self, request: Request):
    #     # Logic to destroy the user's session
    #     pass

    # def get_current_user(self, request: Request) -> dict:
    #     # Logic to retrieve the current user from the session
    #     pass