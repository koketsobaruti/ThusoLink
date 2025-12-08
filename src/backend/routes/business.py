from backend.utils.database.business_db_utils import BusinessDBUtils
from backend.utils.database.db_utils import DBUtils
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Auth Routes")
from ..database.connection import get_db
# import business_manager
from ..modules.business.business_manager import BusinessManager
router = APIRouter(tags=["Business"])
# DB = Session = Depends(get_db)
# db_utils = DBUtils(DB)

@router.post("/get-business-info")
async def get_business_info(name: str, DB: Session = Depends(get_db)):
    logger.info("Get business info endpoint called")
    business_manager = BusinessManager(DB)
    response = business_manager.get_business_by_name(name)
    return response

@router.post("/get-business-services")
async def get_business_services():
    logger.info("Get business services endpoint called")
    return {"message": "business services retrieved successfully"}

@router.post("/update-business-info")
async def update_business_info():
    logger.info("Update business info endpoint called")
    return {"message": "business info updated successfully"}

@router.post("/delete-business")
async def delete_business():
    logger.info("Delete business endpoint called")
    return {"message": "business deleted successfully"}