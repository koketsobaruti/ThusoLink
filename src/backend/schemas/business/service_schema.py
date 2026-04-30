from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from enum import Enum

# ------------------- Currency Enum -------------------
class CurrencyEnum(str, Enum):
    BWP = "BWP"  # Botswana Pula
    ZAR = "ZAR"  # South African Rand
    NGN = "NGN"  # Nigerian Naira
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro

# ------------------- Base Schema -------------------
class BusinessServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: CurrencyEnum = CurrencyEnum.BWP  # default to Pula

# ------------------- Create Schema -------------------
# class BusinessServiceCreate(BusinessServiceBase):
#     business_id: UUID
#     created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ------------------- Update Schema -------------------
class BusinessServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[CurrencyEnum] = None

# ------------------- Response Schema -------------------
class BusinessServiceResponse(BaseModel):
    id: UUID
    business_id: UUID
    name: str
    description: str
    price: float
    currency: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class BusinessServiceListResponse(BaseModel):
    services: list[BusinessServiceResponse]