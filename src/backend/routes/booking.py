from datetime import date, datetime
import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..auth.jwt_bearer import get_current_user, get_current_active_user, oauth2_scheme
from ..utils.logger_utils import LoggerUtils
from ..schemas.business.schedule_schema import SetAvailabilityRequest
from ..models.user.user_model import User
from ..modules.business.schedule_manager import ScheduleManager
from ..database.connection import get_db
from sqlalchemy.orm import Session
logger = LoggerUtils.get_logger("Auth Routes")

router = APIRouter(tags=["Bookings"])

@router.post("/owner/set_slots", dependencies=[Depends(oauth2_scheme)])
async def set_available_slots(request: SetAvailabilityRequest, DB: Session = Depends(get_db), 
                        current_user: User = Depends(get_current_user)):
    schedule_manager = ScheduleManager(DB)
    current_user_id = current_user.id
    logger.info(f"Service ID {request.service_id} \n User ID {current_user_id}")
    response = schedule_manager.set_service_availability(request.service_id, current_user_id, request.slots)
    return response
    # slots = []
    # available_slots = {"service_id": uuid.uuid4(), "slots": []}
    # for slot in request.slots:
    #     # User can set multiple slots of time in one day
    #     for date in slot.dates:
    #         slot_date = datetime.strptime(date, "%Y-%m-%d").date()
    #         slot_times = []
    #         for hour in slot.hours:
    #             # get time in 24hr format
    #             slot_time = datetime.strptime(f"{hour}:00", "%H:%M").time()
    #             slot_times.append(slot_time)
    #         slot = Slot(date=slot_date, times=slot_times)
    
    #     slot_datetime = datetime.combine(slot.date, slot.times[0])  # Use first time in slot
    #     slots.append(slot_datetime)
    

# @router.post("/bookings")
# def create_booking(request: BookingRequest):
#     booking_datetime = datetime.combine(request.day, time(request.hour))
    
#     # Check if service has available slots
#     if request.service_id not in available_slots:
#         raise HTTPException(status_code=400, detail="Service has no available slots set.")
    
#     # Check if slot is available
#     if booking_datetime not in available_slots[request.service_id]:
#         raise HTTPException(status_code=400, detail="Selected slot is not available.")
    
#     # Check if slot is already booked
#     for b in bookings:
#         if b["service_id"] == request.service_id and b["booking_time"] == booking_datetime:
#             raise HTTPException(status_code=400, detail="Slot already booked.")
    
#     # Book slot
#     new_booking = {
#         "booking_id": len(bookings) + 1,
#         "user_id": request.user_id,
#         "service_id": request.service_id,
#         "booking_time": booking_datetime,
#         "status": "confirmed"
#     }
#     bookings.append(new_booking)
#     return new_booking

# @router.post("/update-booking-info")
# async def update_booking_info():
#     logger.info("Update booking  info endpoint called")
#     return {"message": "booking  info updated successfully"}

# @router.post("/delete-booking ")
# async def delete_booking():
#     logger.info("Delete booking  endpoint called")
#     return {"message": "booking  deleted successfully"}