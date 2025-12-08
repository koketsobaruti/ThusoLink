from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, timezone, date, time

class BookingStatus(str):
    confirmed = "confirmed"
    cancelled = "cancelled"
    pending = "pending"

# ------------------- Base Schemas -------------------
class BookingBase(BaseModel):
    service_id: UUID
    
    booking_date: date
    booking_time: time  
    notes: Optional[str] = None

# ------------------- Create Schemas -------------------
class BookingCreate(BookingBase):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ------------------- Update Schemas -------------------
class BookingUpdate(BaseModel):
    booking_date: Optional[date] = None
    booking_time: Optional[time] = None
    notes: Optional[str] = None
    status: Optional[BookingStatus] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ------------------- Response Schemas -------------------
class BookingResponse(BookingBase):
    id: UUID
    status: BookingStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# ------------------- Bulk Slots (for owner) -------------------
class BookingSlot(BaseModel):
    booking_date: date
    booking_time: time

class SetAvailabilityRequest(BaseModel):
    service_id: UUID
    slots: List[BookingSlot]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
