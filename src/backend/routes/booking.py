from datetime import date, datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from ..schemas.business.schedule_schema import AvailabilityFilter
from ..auth.jwt_bearer import get_current_user, get_current_active_user, oauth2_scheme
from ..utils.logger_utils import LoggerUtils
from ..schemas.business.schedule_schema import SetAvailabilityRequest
from ..models.user.user_model import User
from ..models.business.schedule_model import ServiceAvailability, BusinessAvailability
from ..modules.business.schedule_manager import ScheduleManager
from ..database.connection import get_db
from sqlalchemy.orm import Session
logger = LoggerUtils.get_logger("Auth Routes")

router = APIRouter(tags=["Bookings"])

@router.post("/owner/set_service_slots", dependencies=[Depends(oauth2_scheme)])
async def set_service_availablility_slots(request: SetAvailabilityRequest, DB: Session = Depends(get_db), 
                        current_user: User = Depends(get_current_user)):
    schedule_manager = ScheduleManager(DB)
    current_user_id = current_user.id
    logger.info(f"Service ID {request.item_id} \n User ID {current_user_id}")
    response = schedule_manager.set_service_availability(request.item_id, current_user_id, request.slots)
    return response

# @router.get("/get_service_availability", dependencies=[Depends(oauth2_scheme)])
# async def get_service_availailablility(service_id: str, DB: Session = Depends(get_db)):
#     schedule_manager = ScheduleManager(DB)
#     response = schedule_manager.get_service_availability(service_id)
#     return response

@router.post("/owner/set_business_slots", dependencies=[Depends(oauth2_scheme)])
async def set_business_available_slots(request: SetAvailabilityRequest, DB: Session = Depends(get_db), 
                        current_user: User = Depends(get_current_user)):
    schedule_manager = ScheduleManager(DB)
    logger.info(f"Business ID {request.item_id} \n User ID {current_user.id}")
    response = schedule_manager.set_business_availability(request.item_id, current_user.id, request.slots)
    return response

# @router.get("/get_business_availability", dependencies=[Depends(oauth2_scheme)])
# async def get_business_availailablility(business_id: str, DB: Session = Depends(get_db)):
#     schedule_manager = ScheduleManager(DB)
#     response = schedule_manager.get_business_availability(business_id)
#     return response

@router.post("/get_availability_by_filter", dependencies=[Depends(oauth2_scheme)])
async def get_availability_by_filter(filter: AvailabilityFilter, DB: Session = Depends(get_db)):
    schedule_manager = ScheduleManager(DB)
    response = schedule_manager.get_availability_by_filter(filter)
    return response


# @router.post("/update-booking-info")
# async def update_booking_info():
#     logger.info("Update booking  info endpoint called")
#     return {"message": "booking  info updated successfully"}

# @router.post("/delete-booking ")
# async def delete_booking():
#     logger.info("Delete booking  endpoint called")
#     return {"message": "booking  deleted successfully"}