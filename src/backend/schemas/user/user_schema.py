# src/backend/schemas/user_schema.py
from datetime import datetime, timezone
from typing import Annotated, Optional
from fastapi import logger
from pydantic import BaseModel, EmailStr, Field, constr, field_validator, validator
import re
import uuid
from ..timestamps_schema import Timestamps

# def generate_username(full_name: str) -> str:
#     """Generate username from first 3 chars of first name + 9-digit UUID"""
#     first_part = full_name.split(" ")[0][:3].lower()
#     random_part = str(uuid.uuid4().int)[:9]
#     # concatenate to form username

#     logger.info(f"Generated username: {first_part}{random_part}")
#     return f"{first_part}{random_part}"

# ✅ Regex for password:
# Must contain at least:
# - one lowercase letter
# - one uppercase letter
# - one digit
# - one special character
# - minimum 8 characters
password_regex = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"
)
# ✅ Define reusable password type
PasswordStr = Annotated[
    str,
    Field(
        min_length=8,
        pattern=password_regex.pattern,
        description="Must contain uppercase, lowercase, number, and special character"
    ),
]

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: Optional[EmailStr]


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain a lowercase letter")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain an uppercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain a digit")
        if not re.search(r"[@$!%*#?&_]", v):
            raise ValueError("Password must contain a special character")
        return v


# -------------------------
# User read / timestamp model (optional)
# -------------------------
class UserRead(UserBase):
    pass  # inherits all fields from UserBase, including timestamps

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr

    class ConfigDict:
        from_attributes = True
