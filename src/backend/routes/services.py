from ..utils.database.business_db_utils import BusinessDBUtils
from ..utils.database.db_utils import DBUtils
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Services Routes")
from ..database.connection import get_db
# import business_manager
# add service_schema.py
# from ..schemas.business.service_schema import service_schema
# import servicemanager 
from ..modules.business.service_manager import ServiceManager
router = APIRouter(tags=["Services"])

@router.get("/get-business-services")
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
async def add_service():
    logger.info("Add service endpoint called")

    return {"message": "service added successfully"}    

