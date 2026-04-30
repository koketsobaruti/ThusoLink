from fastapi import APIRouter
from ..utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Auth Routes")

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/update-user-info")
async def update_user_info():
    logger.info("Update user info endpoint called")
    return {"message": "User info updated successfully"}

@router.post("/delete-user")
async def delete_user():
    logger.info("Delete user endpoint called")
    return {"message": "User deleted successfully"}