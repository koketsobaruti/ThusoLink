# src/backend/routes/auth_routes.py
from uuid import UUID
from ..schemas.business.service_schema import BusinessServiceCreate
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ..utils.database.db_utils import DBUtils
from ..schemas.business.business_schema import BusinessCreate
from ..schemas.general_response import GeneralResponse
from ..schemas.user.user_schema import UserCreate
# from ..depends.dependencies import get_current_user
from ..auth.jwt_bearer import get_current_user
from ..database.connection import get_db
# import registration manager
from ..modules.auth.registration_manager import RegistrationManager
from ..utils.logger_utils import LoggerUtils
# import User
from ..models.user.user_model import User
from ..models.business.business_model import Business
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
                            current_user: User = Depends(get_current_user), DB: Session = Depends(get_db)):
    # email = current_user.email
    # db_utils = DBUtils(DB)
    user_id = current_user.id
    logger.info(f"Registering business for user ID: {user_id}")
    registration_manager = RegistrationManager(DB)
    response = registration_manager.register_business(business, user_id)
    return response

@router.post("/register-service")
async def register_service(business_id: str, service:BusinessServiceCreate,
                            current_user: User = Depends(get_current_user), DB: Session = Depends(get_db)):
    user_id = current_user.id 
    bus_id = UUID(business_id)
    business = DB.query(Business).filter(Business.id == bus_id).first()
    if business is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found",
        )
    registration_manager = RegistrationManager(DB)
    response = registration_manager.register_service(service, user_id, business.id)
    return response

