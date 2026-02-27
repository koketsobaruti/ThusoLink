from datetime import date, datetime
from typing import Any, Dict
import uuid
from fastapi import APIRouter, Depends, Request, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from ..schemas.business.schedule_schema import AvailabilityFilter, AvailabilityType, SetOffDay
from ..auth.jwt_bearer import get_current_user, get_current_active_user, oauth2_scheme
from ..utils.logger_utils import LoggerUtils
from ..schemas.business.schedule_schema import SetAvailabilityRequest, AvailabilityRequest
from ..models.user.user_model import User
from ..models.business.schedule_model import ServiceAvailability, BusinessAvailability
from ..modules.business.schedule_manager import ScheduleManager
from ..modules.business.booking_manager import BookingManager
from ..schemas.business.bookings_schema import BookingRequest, BookingType, BookingUpdate
from ..database.connection import get_db
from sqlalchemy.orm import Session
logger = LoggerUtils.get_logger("Auth Routes")

router = APIRouter(tags=["Bookings"])

@router.post("/owner/set_availability", dependencies=[Depends(oauth2_scheme)])
async def set_availability_slots(request: AvailabilityRequest, DB: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    schedule_manager = ScheduleManager(DB)
    current_user_id = current_user.id
    logger.info(f"Record ID {request.record_id} \n User ID {current_user_id}")
    response = schedule_manager.set_availability(request, current_user_id)
    return response

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

@router.post("/request-booking")
async def request_booking(request: BookingRequest,
                          background_tasks: BackgroundTasks,
                         db: Session = Depends(get_db),
                         user=Depends(get_current_user)):

    manager = BookingManager(db)

    result = manager.request_booking(
        booking_request=request,
        customer_id=user.id
    )
    # schedule async whatsapp notification
    background_tasks.add_task(
        manager.notify_owner_whatsapp,
        result.data["booking"]
    )
    return result

@router.post("/set_off_day", dependencies=[Depends(oauth2_scheme)])
async def set_off_day(request: SetOffDay, background_tasks: BackgroundTasks
                      , db: Session = Depends(get_db),
                         user=Depends(get_current_user)) :
    if validate_request(request):
        schedule_manager = ScheduleManager(db)
        # logger.info(f"Record ID {request.record_id} \n User ID {user.id}")
        response = schedule_manager.set_off_day(request, user.id)
        
        background_tasks.add_task(
            schedule_manager.update_current_bookings,
            request
        )

        background_tasks.add_task(
            schedule_manager.update_avaialability_status,
            request
        )
    # background_tasks.add_task(
    #     schedule_manager.notify_customers_of_unavailability,
    #     request
    # )

    return response
def validate_request(request: Request):

    if request.request_type not in [AvailabilityType.BUSINESS, AvailabilityType.SERVICE, AvailabilityType.EMPLOYEE]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request type")
    elif not request.off_dates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Off dates must be provided")
    elif not request.record_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Record ID must be provided")
    else:
        return True       
# @router.post("/webhook")
# async def whatsapp_webhook(request: Request, db: Session = Depends(get_current_user)):
#     payload: Dict[str, Any] = await request.json()
#     logger.info(f"Received WhatsApp webhook payload: {payload}")
#     try:
#         entry = payload.get("entry", [])[0]
#         changes = entry[0].get("changes", [])
#         value = changes[0].get("value", {})
#         messages = value.get("messages")

#         if not messages:
#             logger.info("No messages found in the webhook payload.")
#             return {"message": "Webhook received successfully, but no messages to process."}
#         message = messages[0]
#         if message.get("type") != "interactive":
#             return {"status": "not_interactive"}
        
#         button_id = message["interactive"]["button_reply"]["id"]
#         # Process the button_id to update booking status
#         booking_manager = BookingManager(db)
#         if button_id.startswith("accept_"):
#             booking_id = button_id.split("accept_")[1]
            
#             booking_manager.update_booking_status(BookingUpdate(
#                 booking_type=BookingType.SERVICE,  # Adjust based on your logic
#                 booking_id=booking_id,
#                 status=BookingStatus.ACCEPTED.value
#             ), user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"))  # Replace with actual user ID
#     # Process the payload and update booking status accordingly
#     # You would need to implement logic here to parse the payload and update the booking in your database
#     return {"message": "Webhook received successfully"}
# @router.post("/update-booking-info")
# async def update_booking_info():
#     logger.info("Update booking  info endpoint called")
#     return {"message": "booking  info updated successfully"}

# @router.post("/delete-booking ")
# async def delete_booking():
#     logger.info("Delete booking  endpoint called")
#     return {"message": "booking  deleted successfully"}