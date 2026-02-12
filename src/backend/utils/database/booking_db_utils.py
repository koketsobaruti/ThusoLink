from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Union
from sqlalchemy import text, select, and_
from ...schemas.business.schedule_schema import AvailabilityStatus
from ...schemas.business.bookings_schema import BookingRequest, BookingStatus, BookingUpdate
from sqlalchemy.exc import SQLAlchemyError
from ...models.business.service_model import BusinessService
from ...schemas.business.service_schema import BusinessServiceResponse
from ...schemas.business.business_schema import BusinessCreate, BusinessEmailResponse, BusinessLocationResponse, BusinessPhoneResponse, BusinessResponse, BusinessSocialResponse, BusinessUpdate
from ...models.business.business_model import BusinessEmail, BusinessLocation, BusinessPhone, BusinessSocial, Business
from ...utils.logger_utils import LoggerUtils
from ...config.booking_map import BOOKING_REGISTRY
from ...models.business.schedule_model import Availability
from ...utils.database.business_db_utils import BusinessDBUtils
from ...models.business.booking_model import ServiceBooking, BusinessBooking, Booking
from ...schemas.business.bookings_schema import BookingResponse, WhatsAppBookingDetails
logger = LoggerUtils.get_logger("Booking DB Utils")
class BookingDBUtils:
    def __init__(self, db: Session):
        self.db = db
        self.business_db_utils = BusinessDBUtils(self.db)

    def get_slot(self, availability_id):
         # Fetch the slot
        try:
            slot = self.db.query(Availability)\
                    .filter(Availability.id == availability_id)\
                    .with_for_update()\
                    .first()        
            if not slot:
                raise HTTPException(status_code=404, detail="Slot not found")

            if slot.availability_status != AvailabilityStatus.AVAILABLE:
                raise HTTPException(status_code=400, detail="Slot is no longer available")
            
            slot.availability_status = AvailabilityStatus.REQUESTED
            return slot
        except Exception as e:
            logger.error(f"Error fetching slot: {str(e)}")    
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking slot existence: {str(e)}"
            )
        
    def save_booking(self, slot, customer_id, booking_request: BookingRequest):
        try:
            new_booking = Booking(
                availability_id=slot.id,
                customer_id=customer_id,
                customization=booking_request.customization,
                notes=booking_request.notes,
                # inspiration_images=booking_request.inspiration_images,
                status=BookingStatus.REQUESTED,
                booking_type=booking_request.availability_type.value
            )
            try:
                self.db.add(new_booking)

                # 🔥 UPDATE AVAILABILITY STATUS
                slot.availability_status = AvailabilityStatus.REQUESTED

                # 💾 SINGLE COMMIT
                self.db.commit()

                self.db.refresh(new_booking)
                self.db.refresh(slot)
                # get the booking ID after commit and map to response schema

                booking_response = BookingResponse(
                    id=str(new_booking.id),
                    availability_type=booking_request.availability_type.value,
                    availability_id=str(new_booking.availability_id),
                    customer_id=str(new_booking.customer_id),
                    date=slot.date.isoformat(),
                    start_time=slot.start_time.isoformat(),
                    end_time=slot.end_time.isoformat(),
                    availability_status=slot.availability_status.value,
                    customization=new_booking.customization,
                    notes=new_booking.notes,
                    # inspiration_images=new_booking.inspiration_images,
                    status=new_booking.status.value
                )
                # logger.info(f"Created booking: {booking_response}")
                return booking_response
            except SQLAlchemyError as e:
                self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to persist availability slots : {e}.",
                )

        except Exception as e:
            logger.error(f"Error setting booking in DB: {str(e)}")    
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error setting up booking: {str(e)}"
            )


    def fetch_slot(self, AvailabilityModel, availability_id):
         # Fetch the slot
        try:
            slot = self.db.query(AvailabilityModel)\
                    .filter(AvailabilityModel.id == availability_id)\
                    .with_for_update()\
                    .first()        
            if not slot:
                raise HTTPException(status_code=404, detail="Slot not found")

            if slot.availability_status != AvailabilityStatus.AVAILABLE:
                raise HTTPException(status_code=400, detail="Slot is no longer available")
            
            slot.availability_status = AvailabilityStatus.REQUESTED
            return slot
        except Exception as e:
            logger.error(f"Error fetching slot: {str(e)}")    
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking slot existence: {str(e)}"
            )
    
    def create_booking(self, BookingModel, slot, customer_id, booking_request: BookingRequest):
        try:
            new_booking = BookingModel(
                availability_id=slot.id,
                customer_id=customer_id,
                customization=booking_request.customization,
                notes=booking_request.notes,
                # inspiration_images=booking_request.inspiration_images,
                status=BookingStatus.REQUESTED
            )
            try:
                self.db.add(new_booking)

                # 🔥 UPDATE AVAILABILITY STATUS
                slot.availability_status = AvailabilityStatus.REQUESTED

                # 💾 SINGLE COMMIT
                self.db.commit()

                self.db.refresh(new_booking)
                self.db.refresh(slot)
                # get the booking ID after commit and map to response schema

                booking_response = BookingResponse(
                    id=str(new_booking.id),
                    availability_type=booking_request.availability_type.value,
                    availability_id=str(new_booking.availability_id),
                    customer_id=str(new_booking.customer_id),
                    date=slot.date.isoformat(),
                    start_time=slot.start_time.isoformat(),
                    end_time=slot.end_time.isoformat(),
                    availability_status=slot.availability_status.value,
                    customization=new_booking.customization,
                    notes=new_booking.notes,
                    # inspiration_images=new_booking.inspiration_images,
                    status=new_booking.status.value
                )
                # logger.info(f"Created booking: {booking_response}")
                return booking_response
            except SQLAlchemyError as e:
                self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to persist availability slots : {e}.",
                )

        except Exception as e:
            logger.error(f"Error setting booking in DB: {str(e)}")    
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error setting up booking: {str(e)}"
            )
    def get_provider_and_phone(self, booking:BookingRequest):
        try:
            config = BOOKING_REGISTRY[booking.availability_type]
            if not config:
                raise ValueError(f"No booking configuration found for type: {booking.availability_type}")
            
            query ="""SELECT record_id from availability where id=:availability_id"""
            record_id = self.db.execute(text(query), {"availability_id": booking.availability_id}).scalar()
                
            if booking.availability_type == "business":
                business_details = self.business_db_utils.get_business_by_id(record_id)
                if not business_details:
                    raise ValueError(f"Business with ID {record_id} not found")
                phones = business_details.get("phones") or []
                phone_number = phones[0].number
                if not phone_number:
                    raise ValueError(f"WhatsApp number not found for business ID {record_id}")
            if booking.availability_type == "service":
                query ="""SELECT business_id from business_services where id=:record_id"""
                business_id = self.db.execute(text(query), {"record_id": record_id}).scalar()
                business_details = self.business_db_utils.get_business_by_id(business_id)
                if not business_details:
                    raise ValueError(f"Business with ID {business_id} not found")
                phones = business_details.get("phones") or []
                phone_number = phones[0].number
                if not phone_number:
                    raise ValueError(f"WhatsApp number not found for business ID {business_id}")
            results = {"provider": business_details, "phone": phone_number}
            return results
        except Exception as e:
            logger.error(f"Error fetching provider and WhatsApp: {str(e)}")  
            raise ValueError(f"Failed to get provider or WhatsApp number: {e}")
   
    def get_provider_and_phone2(self, booking:BookingRequest):
        """
        Given an availability object (Service/Business/Staff),
        returns the provider record and the WhatsApp number.
        All errors are caught and raised as descriptive ValueErrors.
        """

        try:
            # logger.info(f"Fetching provider and WhatsApp for booking: {booking}")
            config = BOOKING_REGISTRY[booking.availability_type]
            
            # BookingModel = config["booking_model"]
            AvailabilityModel = config["availability_model"]
            provider_field = config["provider_field"]

            # fk_field = getattr(BookingModel, "fk_field", None)
            # provider_id = getattr(booking, fk_field, None)

            # if not fk_field or not provider_id:
            #     raise ValueError(f"Availability missing fk_field or provider ID: {availability.id}")

            # Fetch provider safely
            availability = self.db.query(AvailabilityModel).filter(
                AvailabilityModel.id == booking.availability_id
            ).first()

            provider_id = getattr(availability, provider_field)
            if provider_field == "service_id":
                provider_details = self.db.query(BusinessService).filter(BusinessService.id == provider_id).first()
                if not provider_details:
                    raise ValueError(f"Service with ID {provider_id} not found")
                business_id = provider_details.business_id
                provider_response = BusinessServiceResponse.model_validate(provider_details)
                # map provider_details to BusinessServiceResponse
                

            elif provider_field == "business_id":
                provider_details = self.db.query(Business).filter(Business.id == provider_id).first()
                if not provider_details:
                    raise ValueError(f"Business with ID {provider_id} not found")
                business_id = provider_details.id
                provider_response = self.business_db_utils.get_business_by_name(provider_details.name)
            else:
                raise ValueError(f"Unknown provider type: {provider_field}")

            # Fetch WhatsApp number safely
            phone_record = self.db.query(BusinessPhone).filter(
                BusinessPhone.business_id == business_id
            ).first()
            if not phone_record or not phone_record.number:
                raise ValueError(f"WhatsApp number not found for business ID {business_id}")

            results = {"provider": provider_response, "phone": phone_record.number}
            return results

        except Exception as e:
            # Optionally log the error here
            logger.error(f"Error fetching provider and WhatsApp: {e}")
            # Raise a controlled exception so calling code can handle it
            raise ValueError(f"Failed to get provider or WhatsApp number: {e}")

    def get_booking_by_id(self, booking_id: str) -> Union[ServiceBooking, BusinessBooking]:
        try:
            query ="""SELECT * FROM service_bookings, business_bookings WHERE id = :booking_id"""
            booking_record = self.db.query()
            for booking_type, config in BOOKING_REGISTRY.items():
                BookingModel = config["booking_model"]
                booking = self.db.query(BookingModel).filter(BookingModel.id == booking_id).first()
                if booking:
                    return booking
            raise HTTPException(status_code=404, detail="Booking not found")
        except Exception as e:
            logger.error(f"Error fetching booking by ID: {str(e)}")    
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
    def check_booking_exists(self, bookingModel, booking_id) -> bool:
        try:
            booking = self.db.query(bookingModel).filter(bookingModel.id == booking_id).first()
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")
            
            return booking
        except Exception as e:
            logger.error(f"Error checking if booking exists: {str(e)}")    
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )