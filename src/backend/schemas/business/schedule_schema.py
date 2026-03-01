from typing import List, Optional
from uuid import UUID
import uuid
from pydantic import BaseModel, ValidationError, field_validator
import enum
from datetime import date, time

class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = "available"
    REQUESTED = "requested"
    BOOKED = "booked"
    COMPLETED = "completed"
    UNAVAILABLE = "unavailable"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"
    EXPIRED = "expired"
    

class AvailabilityType(str, enum.Enum):
    BUSINESS = "business"
    SERVICE = "service"
    EMPLOYEE = "employee"

class AvailabilitySlot(BaseModel):
    date: date
    start_time: time
    end_time: Optional[time] = None
    availability_status: Optional[AvailabilityStatus] = None

class AvailabilityRequest(BaseModel):
    record_id:str
    request_type:AvailabilityType
    slots: List[AvailabilitySlot]

class SetAvailabilityRequest(BaseModel):
    item_id: str
    slots: List[AvailabilitySlot]

class GetByAvailabilityStatus(BaseModel):
    item_id: str
    availability_status: str = None

class AvailabilityFilter(BaseModel):
    availability_type: Optional[AvailabilityType] = None  # "business", "service", "employee"
    record_id: Optional[UUID] = None
    selected_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    availability_status: Optional[str] = None


class AvailabilityResponse(BaseModel):
    id: UUID
    record_id: UUID
    date: date
    start_time: time
    end_time: time
    availability_status: str

class SetOffDay(BaseModel):
    record_id: UUID
    request_type: AvailabilityType
    off_dates: list[date]
    
    @field_validator("off_dates")
    @classmethod
    def validate_off_dates(cls, value):
        if not value:
            raise ValueError("At least one off date must be provided")

        if any(d < date.today() for d in value):
            raise ValueError("Off dates cannot be in the past")

        if len(set(value)) != len(value):
            raise ValueError("Duplicate off dates are not allowed")

        return value
    
    @field_validator("request_type")
    @classmethod
    def validate_request_type(cls, value):
        if value not in [type.item in AvailabilityRequest]:
            raise  ValueError("Select appropriate availability request")
        if value is None:
            raise ValueError("Input value for availability request")