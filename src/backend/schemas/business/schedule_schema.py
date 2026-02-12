from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
import enum
from datetime import date, time

class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = "available"
    REQUESTED = "requested"
    BOOKED = "booked"
    COMPLETED = "completed"

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
    availability_type: AvailabilityType  # "business", "service", "employee"
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