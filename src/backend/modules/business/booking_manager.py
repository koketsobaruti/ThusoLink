from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
from uuid import uuid4
from fastapi import HTTPException, requests, status
from ...models.business.service_model import BusinessService
from ...schemas.business.service_schema import BusinessServiceCreate, BusinessServiceListResponse, BusinessServiceResponse
from ...schemas.general_response import GeneralResponse
from ...utils.database.db_utils import DBUtils
from ...utils.availability_utils import check_availability_input
from ...schemas.business.schedule_schema import AvailabilityFilter,AvailabilityStatus, AvailabilityResponse
from ...utils.database.service_db_utils import ServiceDBUtils
from ...schemas.business.bookings_schema import BookingRequest, BookingStatus, BookingUpdate, WhatsAppBookingDetails
from ...utils.database.booking_db_utils import BookingDBUtils
from ...models.business.business_model import Business, BusinessPhone
from sqlalchemy.orm import Session
from ...config.availability_map import AVAILABILITY_MAP
from ...config.booking_map import BOOKING_REGISTRY
from ...config.config import Settings
from ...utils.logger_utils import LoggerUtils
from ...services.whatsapp.whatsapp_services import WhatsAppService
from ...services import client, messages, client
from uuid import UUID
logger = LoggerUtils.get_logger("Booking Manager")
class BookingManager:
    def __init__(self, db: Session):
        self.db = db
        self.service_db_utils = ServiceDBUtils(self.db)
        self.general_db_utils = DBUtils(self.db)
        self.booking_db_utils = BookingDBUtils(self.db)
        self.whatsapp_service = WhatsAppService()

    def request_booking(self, booking_request: BookingRequest, customer_id: UUID)-> GeneralResponse:
        try:
            # Get the model for this type
            if booking_request.availability_type.value not in AVAILABILITY_MAP:
                raise HTTPException(status_code=400, detail="Invalid availability type")
            config = BOOKING_REGISTRY[booking_request.availability_type.value]

            AvailabilityModel = config["availability_model"]
            BookingModel = config["booking_model"]
            # Update slot to REQUESTED
            slot = self.booking_db_utils.fetch_slot(AvailabilityModel=AvailabilityModel, availability_id=booking_request.availability_id)
            
            created_booking = self.booking_db_utils.create_booking(BookingModel=BookingModel,booking_request=booking_request, slot=slot, customer_id=customer_id)
            # map created booking to response schema
            
            # Build and return the API response with the booking
            return GeneralResponse(
                status=status.HTTP_200_OK,
                message="Booking requested successfully",
                data={"booking": created_booking}
                )
        except Exception as e:
            logger.error(f"Error reacting a booking request: {str(e)}")    
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
    
    def get_whatsapp_booking_details(self, booking):
        try:
            customer = self.general_db_utils.get_current_username(booking.customer_id)
            # availability = booking.availability

            results = self.booking_db_utils.get_provider_and_phone(booking=booking)
            provider= results.get("provider")
            # logger.info(f"Provider details for booking {booking.id}: {provider}")
            whatsapp_booking_details = WhatsAppBookingDetails(booking_id=str(booking.id),
                                                            customer_name=customer.full_name,
                                                            slot_date=booking.date,
                                                            slot_start_time=booking.start_time,
                                                            slot_end_time=booking.end_time,
                                                            provider_name=provider.name,
                                                            provider_whatsapp_number=results["phone"],
                                                            customization=booking.customization,
                                                            notes=booking.notes,
                                                            # inspiration_images=booking.inspiration_images,
                                                            status=booking.status.value
                                                        )
            logger.info(f"WhatsApp booking details for booking {booking.id}: {whatsapp_booking_details}")
            return whatsapp_booking_details
        except Exception as e:
            logger.error(f"Error reacting a booking request: {str(e)}")    
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
    def build_whatsapp_message(self, details: WhatsAppBookingDetails):
        start_time = details.slot_start_time
        end_time = details.slot_end_time

            # Decide how to display time
        if start_time == end_time:
            time_str = start_time.strftime("%H:%M")
        else:
            time_str = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

        body = (
            f"New booking request from {details.customer_name}.\n"
            f"Date: {details.slot_date}, Appointment time: {time_str}\n"
            f"Provider: {details.provider_name}\n"
        )
        if details.customization:
            body += f"Customization: {details.customization}\n"
        if details.notes:
            body += f"Notes: {details.notes}\n"
        # if details['inspiration_images']:
        #     body += f"Inspiration images: {', '.join(details['inspiration_images'])}\n"
        return body

    async def notify_owner_whatsapp(self, booking:BookingRequest):
        try: 
            details = self.get_whatsapp_booking_details(booking)

            message_text = self.build_whatsapp_message(details)
            # logger.info(f"Whatsapp message for booking {booking.id}: \n {message_text}")
            await self.whatsapp_service.send_booking_request(
                booking=booking,
                message_text=message_text
            )
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
    def update_booking_status(self, booking_id:str):
        try:
            get_booking = self.booking_db_utils.get_booking_by_id(booking_id)
    # def update_booking_status(self, bookingUpdate: BookingUpdate, user_id: UUID) -> GeneralResponse:
    #     try:
    #         bookingModel = BOOKING_REGISTRY[bookingUpdate.availability_type.value]["booking_model"]
    #         booking = self.booking_db_utils.check_booking_exists(bookingModel, bookingUpdate.booking_id)
    #         slot = self.db.query(bookingModel).filter(
    #             bookingModel.id == booking.availability_id
    #         ).first()
    #         booking_id = bookingUpdate.booking_id
    #         status = bookingUpdate.status

    #         if status not in BookingStatus._value2member_map_:
    #             raise HTTPException(status_code=400, detail="Invalid booking status")
    #         booking = self.booking_db_utils.get_booking_by_id(booking_id)
    #         if not booking:
    #             raise HTTPException(status_code=404, detail="Booking not found")
    #         # Check if the user is authorized to update this booking
    #         if booking.customer_id != user_id and not self.booking_db_utils.is_user_provider_for_booking(booking_id, user_id):
    #             raise HTTPException(status_code=403, detail="Not authorized to update this booking")
    #         updated_booking = self.booking_db_utils.update_booking_status(booking_id, status)
    #         return GeneralResponse(
    #             status=status.HTTP_200_OK,
    #             message="Booking status updated successfully",
    #             data={"booking": updated_booking}
    #         )
    #     except HTTPException as e:
    #         raise e
    #     except Exception as e:
    #         logger.error(f"Error updating booking status: {str(e)}")    
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=f"An error occurred: {str(e)}",
    #             headers={"WWW-Authenticate": "Bearer"}
    #         )
    
    
    # def notify_owner_whatsapp(self, booking):
    #     details = self.get_whatsapp_booking_details(booking)
    #     message_text = self.build_whatsapp_message(details)
    #     url = f"https://graph.facebook.com/v17.0/{Settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    #     headers = {
    #         "Authorization": f"Bearer {Settings.WHATSAPP_TOKEN}",
    #         "Content-Type": "application/json"
    #     }

    #     data = {
    #         "messaging_product": "whatsapp",
    #         "to": details["provider_whatsapp_number"],
    #         "type": "interactive",
    #         "interactive": {
    #             "type": "button",
    #             "body": {"text": message_text},
    #             "action": {
    #                 "buttons": [
    #                     {"type": "reply", "reply": {"id": f"accept_{booking.id}", "title": "Accept"}},
    #                     {"type": "reply", "reply": {"id": f"reject_{booking.id}", "title": "Reject"}}
    #                 ]
    #             }
    #         }
    #     }

    #     try:
    #         response = requests.post(url, json=data, headers=headers)
    #         response.raise_for_status()
    #     except Exception as e:
    #         print(f"Failed to send WhatsApp message: {e}")