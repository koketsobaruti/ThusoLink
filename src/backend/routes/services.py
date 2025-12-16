from backend.depends.dependencies import get_current_user
from backend.modules.auth.registration_manager import RegistrationManager
from backend.modules.auth.registration_manager import RegistrationManager
from backend.utils.database.business_db_utils import BusinessDBUtils
from backend.utils.database.db_utils import DBUtils
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Services Routes")
from ..database.connection import get_db
# import business_manager
# add service_schema.py
import backend.schemas.business.service_schema as service_schema
# import servicemanager 
from backend.modules.business.service_manager import ServiceManager
router = APIRouter(tags=["Services"])

@router.post("/get-business-services")
async def get_business_services(business_name: str, DB: Session = Depends(get_db)):
    logger.info("Get business services endpoint called")
    service_manager = ServiceManager(DB)
    response = service_manager.view_all_services(business_name)
    return response

@router.post("/update-services-info")
async def update_services_info():
    logger.info("Update services info endpoint called")
    return {"message": "services info updated successfully"}

@router.post("/delete-service")
async def delete_service():
    logger.info("Delete service endpoint called")
    return {"message": "service deleted successfully"}

@router.post("/add-service")
async def add_service(request: Request, business_name: str, service:service_schema.BusinessServiceCreate,
                            current_user: dict = Depends(get_current_user), DB: Session = Depends(get_db)):
    db_utils = DBUtils(DB)
    user_id = db_utils.get_current_user_id(current_user['username'])
    business_id = db_utils.get_business_id(business_name)
    registration_manager = RegistrationManager(DB)
    response = registration_manager.register_service(service, user_id, business_id)
    return response

