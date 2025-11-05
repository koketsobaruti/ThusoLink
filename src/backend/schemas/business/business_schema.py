from enum import Enum
import re
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo, validator
from typing import List, Optional
from datetime import datetime, timezone

# ------------------- Enum for Social Platforms -------------------
class SocialPlatform(str, Enum):
    tiktok = "tiktok"
    instagram = "instagram"
    facebook = "facebook"

# ------------------- Base Schemas -------------------
class BusinessBase(BaseModel):
    name: str
    description: Optional[str] = None

class BusinessLocationBase(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    created_at: Optional[datetime] = None

class BusinessSocialBase(BaseModel):
    platform: SocialPlatform
    handle: str
    created_at: Optional[datetime] = None

class BusinessPhoneBase(BaseModel):
    country_code: str
    number: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("number", check_fields=True)
    def validate_phone(cls, v, values: ValidationInfo):
        if not v:
            raise ValueError("Number is required for phone contacts")
        pattern = r"^\+?[1-9]\d{1,14}$"  # E.164 format
        if not re.match(pattern, v):
            raise ValueError(f"Invalid phone number format: {v}")
        return v

class BusinessEmailBase(BaseModel):
    email: EmailStr
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ------------------- Create Schemas -------------------
class BusinessPhoneCreate(BusinessPhoneBase):
    pass

class BusinessEmailCreate(BusinessEmailBase):
    pass

class BusinessLocationCreate(BusinessLocationBase):
    pass

class BusinessSocialCreate(BusinessSocialBase):
    pass

class BusinessCreate(BusinessBase):
    phones: Optional[List[BusinessPhoneCreate]] = []
    emails: Optional[List[BusinessEmailCreate]] = []
    locations: Optional[List[BusinessLocationCreate]] = []
    socials: Optional[List[BusinessSocialCreate]] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ------------------- Update Schemas -------------------
class BusinessPhoneUpdate(BaseModel):
    country_code: Optional[str] = None
    number: Optional[str] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BusinessEmailUpdate(BaseModel):
    email: Optional[EmailStr] = None  # optional for updating existing email

class BusinessLocationUpdate(BaseModel):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BusinessSocialUpdate(BaseModel):
    platform: Optional[SocialPlatform] = None
    handle: Optional[str] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    phones: Optional[List[BusinessPhoneUpdate]] = None
    emails: Optional[List[BusinessEmailUpdate]] = None
    locations: Optional[List[BusinessLocationUpdate]] = None
    socials: Optional[List[BusinessSocialUpdate]] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ------------------- Response Schemas -------------------
class BusinessPhoneResponse(BusinessPhoneCreate):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class BusinessEmailResponse(BusinessEmailCreate):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class BusinessLocationResponse(BusinessLocationCreate):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class BusinessSocialResponse(BusinessSocialCreate):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class BusinessResponse(BusinessBase):
    id: UUID
    owner_id: UUID
    phones: List[BusinessPhoneResponse] = []
    emails: List[BusinessEmailResponse] = []
    locations: List[BusinessLocationResponse] = []
    socials: List[BusinessSocialResponse] = []
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

