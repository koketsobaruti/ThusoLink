from uuid import UUID
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional, List
from datetime import datetime, timezone, date, time
from enum import Enum
from .schedule_schema import AvailabilityType

class BookingStatus(str, Enum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    COMPLETE = "complete"
    UNAVAILABLE = "unavailable"
    RESCHEDULE_REQUIRED = "reschedule_required"

class BookingRequest(BaseModel):
    availability_type: AvailabilityType
    availability_id: str
    customization: Optional[str] = None
    notes: Optional[str] = None
    # inspiration_images: Optional[List[str]] = None

class BookingResponse(BaseModel):
    id: str
    availability_type: str
    availability_id: str
    customer_id: str
    date: str
    start_time: str
    end_time: str
    availability_status: str
    customization: Optional[str] = None
    notes: Optional[str] = None
    # inspiration_images: Optional[List[str]] = None
    status: BookingStatus

class WhatsAppBookingDetails(BaseModel):
    booking_id: str
    customer_name: str
    slot_date: date
    slot_start_time: time
    slot_end_time: time
    provider_name: str
    provider_whatsapp_number: str
    customization: Optional[str] = None
    notes: Optional[str] = None
    # inspiration_images: Optional[List[str]] = None
    status: str

class BookingType(str, Enum):
    SERVICE = "service"
    BUSINESS = "business"
    STAFF = "staff"
    
class BookingUpdate(str, Enum):
    booking_type = BookingType
    booking_id: str

class WhatsappBookingPayLoad(BaseModel):
    message_text: str
    booking_id: str
    to_number: str

class GetBooking(BaseModel):
    record_id:UUID 
    column_name: str
    vals: list[date]
    
    @field_validator("vals")
    @classmethod
    def validate_off_dates(cls, value):
        if not value:
            raise ValueError("At least one value must be provided")
        return value
    
    @field_validator("column_name")
    @classmethod
    def validate_request_type(cls, value):
        if not isinstance(value, str):
            raise ValueError("Input a valid input for column name")
        if not value:
            raise ValueError("The column name must be input")
        return value
    
    @field_validator("record_id")
    @classmethod
    def validate_record_id(cls, value):
        if not UUID(str(value)):
            raise ValidationError("Invalid request input for the record id")
        if not value:
            raise ValueError("The record id must not be null")
        return value

class UpdateBookings(BaseModel):
    booking_id: list[UUID]
    status_value: BookingStatus

    @field_validator("booking_id")
    @classmethod
    def validate_booking_id(cls, value):
        if not value:
            raise ValueError("The booking id must not be null")
        for booking_id in value:
            if not isinstance(booking_id, UUID):
                raise ValueError("Invalid booking id")

        return value
    
    @field_validator("status_value")
    @classmethod
    def validate_status_type(cls, option):
        if option not in [e.value for e in BookingStatus]:
            raise  ValueError("Select appropriate booking status")
        if option is None:
            raise ValueError("Input value for booking status")
        return option