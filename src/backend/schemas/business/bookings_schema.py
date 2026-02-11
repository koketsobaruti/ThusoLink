from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, timezone, date, time
from enum import Enum
from .schedule_schema import AvailabilityType
class BookingStatus(str, Enum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    COMPLETE = "complete"

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