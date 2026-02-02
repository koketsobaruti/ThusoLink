from typing import List, Optional
from pydantic import BaseModel
import enum
from datetime import date, time

class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = "available"
    REQUESTED = "requested"
    BOOKED = "booked"
    COMPLETED = "completed"

class AvailabilitySlot(BaseModel):
    date: date
    start_time: time
    end_time: Optional[time] = None
    availability_status: Optional[AvailabilityStatus] = None


class SetAvailabilityRequest(BaseModel):
    service_id: str
    slots: List[AvailabilitySlot]

