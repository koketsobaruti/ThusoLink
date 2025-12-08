from backend.utils.database.business_db_utils import BusinessDBUtils
from backend.utils.database.db_utils import DBUtils
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Auth Routes")
from ..database.connection import get_db
# import business_manager
# add service_schema.py
import backend.schemas.business.service_schema as service_schema
router = APIRouter(tags=["Servies"])

@router.post("/get-business-services")
async def get_business_services():
    logger.info("Get business services endpoint called")
    return {"message": "business services retrieved successfully"}

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

