# src/backend/routes/auth_routes.py
from backend.schemas.business.service_schema import BusinessServiceCreate
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

router = APIRouter(tags=["Registrations"])
# DB = Session = Depends(get_db)
# db_utils = DBUtils(DB)

@router.post("/register-user", response_model=GeneralResponse)
async def register_user(user: UserCreate, DB: Session = Depends(get_db)):
    registration_manager = RegistrationManager(DB)
    response = registration_manager.register_user(user)
    return response

@router.post("/register-business")
async def register_business(request: Request, business:BusinessCreate, 
                            current_user: dict = Depends(get_current_user), DB: Session = Depends(get_db)):
    email = current_user['username']
    db_utils = DBUtils(DB)
    user_id = db_utils.get_current_user_id(email)
    logger.info(f"Registering business for user ID: {user_id}")
    registration_manager = RegistrationManager(DB)
    response = registration_manager.register_business(business, user_id)
    return response

@router.post("/register-service")
async def register_service(request: Request, business_name: str, service:BusinessServiceCreate,
                            current_user: dict = Depends(get_current_user), DB: Session = Depends(get_db)):
    db_utils = DBUtils(DB)
    user_id = db_utils.get_current_user_id(current_user['username'])
    business_id = db_utils.get_business_id(business_name)
    registration_manager = RegistrationManager(DB)
    response = registration_manager.register_service(service, user_id, business_id)
    return response

