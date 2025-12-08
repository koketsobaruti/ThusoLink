# from datetime import datetime
# from backend.depends.dependencies import get_current_user
# from backend.schemas.business.bookings_schema import BookingBase
# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from ..utils.logger_utils import LoggerUtils
# logger = LoggerUtils.get_logger("Auth Routes")

# router = APIRouter(tags=["Bookings"])

# class BookingRequest(BaseModel):
#     booking_time: datetime  # ISO 8601 datetime, e.g., "2025-12-05T16:00:00"

# @router.post("/user/create_booking")
# def create_booking(booking: BookingBase, current_user: dict = Depends(get_current_user)):


# @router.post("/owner/set_slots")
# def set_available_slots(request: SetAvailabilityRequest):
#     slots = []
#     for slot in request.slots:
#         slot_datetime = datetime.combine(slot.day, time(slot.hour))
#         slots.append(slot_datetime)
    
#     available_slots[request.service_id] = slots
#     return {"message": f"Available slots for service {request.service_id} updated.", "slots": slots}

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