from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

# ------------------- Currency Enum -------------------
class CurrencyEnum(str, Enum):
    BWP = "BWP"  # Botswana Pula
    ZAR = "ZAR"  # South African Rand
    NGN = "NGN"  # Nigerian Naira
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro

# ------------------- Base Schema -------------------
class BusinessServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: CurrencyEnum = CurrencyEnum.BWP  # default to Pula

# ------------------- Create Schema -------------------
class BusinessServiceCreate(BusinessServiceBase):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

# ------------------- Update Schema -------------------
class BusinessServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[CurrencyEnum] = None

# ------------------- Response Schema -------------------
class BusinessServiceResponse(BusinessServiceBase):
    id: UUID
    business_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
