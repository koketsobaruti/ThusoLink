# from backend.utils.database.business_db_utils import BusinessDBUtils
# import BusinessDBUtils  # noqa: F401
from ..utils.database.business_db_utils import BusinessDBUtils
from ..utils.database.db_utils import DBUtils
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Auth Routes")
from ..database.connection import get_db
from ..auth.jwt_bearer import get_current_user, get_current_active_user
from ..modules.business.business_manager import BusinessManager
router = APIRouter(tags=["Business"])
# DB = Session = Depends(get_db)
# db_utils = DBUtils(DB)

@router.post("/get-business-info")
async def get_business_info(name: str, DB: Session = Depends(get_db), 
                            current_user: dict = Depends(get_current_active_user)):
    current_user_id = current_user.id
    if not current_user_id:
        logger.error("Unauthorized access attempt to get business info")
        return {"status": 401, "message": "Unauthorized"}
    business_manager = BusinessManager(DB)
    response = business_manager.get_business_by_name(name)
    return response

@router.post("/get-user-businesses")
async def get_user_businesses(DB: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.info("Get user businesses endpoint called")
    user_id = current_user.id
    business_manager = BusinessManager(DB)
    response = business_manager.get_businesses_by_user(user_id)
    return response

@router.post("/update-business-info")
async def update_business_info():
    logger.info("Update business info endpoint called")
    return {"message": "business info updated successfully"}

@router.post("/delete-business")
async def delete_business():
    logger.info("Delete business endpoint called")
    return {"message": "business deleted successfully"}