# src/backend/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ..utils.database.db_utils import DBUtils
from ..schemas.business.business_schema import BusinessCreate
from ..schemas.general_response import GeneralResponse
from ..schemas.user.user_schema import UserCreate
from ..depends.dependencies import get_current_user
from ..database.connection import get_db
# import registration manager
from ..modules.auth.registration_manager import RegistrationManager
from ..utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Auth Routes")

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register-user", response_model=GeneralResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    registration_manager = RegistrationManager(db)
    response = registration_manager.register_user(user)
    return response

@router.post("/register-business")
async def register_business(request: Request, business:BusinessCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # check if there is a user in the session
    # get the id of the current user from the db
    # user = request.session.get("user")
    # logger.info(f"Regisdtering business for user: {user}")
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    email = current_user['username']
    db_utils = DBUtils(db)
    user_id = db_utils.get_current_user_id(email)
    logger.info(f"Registering business for user ID: {user_id}")
    registration_manager = RegistrationManager(db)
    response = registration_manager.register_business(business, user_id)
    return response