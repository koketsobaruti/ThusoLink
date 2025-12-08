import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum
from backend.database.connection import Base
from ...schemas.business.business_schema import SocialPlatform

# ------------------- Business Model -------------------
class Business(Base):
    __tablename__ = "business"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


    # Relationships
    owner = relationship("User", back_populates="businesses")
    services = relationship("BusinessService", back_populates="business")
    phones = relationship("BusinessPhone", back_populates="businesses", cascade="all, delete-orphan")
    emails = relationship("BusinessEmail", back_populates="businesses", cascade="all, delete-orphan")
    # contacts = relationship("BusinessContact", back_populates="businesses", cascade="all, delete-orphan")
    locations = relationship("BusinessLocation", back_populates="businesses", cascade="all, delete-orphan")
    socials = relationship("BusinessSocial", back_populates="businesses", cascade="all, delete-orphan")

# ------------------- BusinessContact -------------------
# class BusinessContact(Base):
#     __tablename__ = "business_contacts"
#     __table_args__ = {"extend_existing": True} 

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     business_id = Column(UUID(as_uuid=True), ForeignKey("business.id", ondelete="CASCADE"))
#     contact_type = Column(String(50), nullable=False)  # 'phone' or 'email'
#     value = Column(String(255), nullable=True)
#     country_code = Column(String(10), nullable=True)
#     number = Column(String(50), nullable=True)
#     email = Column(String(255), nullable=True)

#     created_at = Column(DateTime(timezone=True))
#     updated_at = Column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc),
#         onupdate=lambda: datetime.now(timezone.utc),
#     )

#     businesses = relationship("Business", back_populates="contacts")
class BusinessPhone(Base):
    __tablename__ = "business_phone"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    country_code = Column(String(10), nullable=False)
    number = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),  
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    businesses = relationship("Business", back_populates="phones")

class BusinessEmail(Base):
    __tablename__ = "business_email"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),    
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),)

    businesses = relationship("Business", back_populates="emails")
# ------------------- BusinessLocation -------------------
class BusinessLocation(Base):
    __tablename__ = "business_locations"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("business.id", ondelete="CASCADE"))
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=True)

    created_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    businesses = relationship("Business", back_populates="locations")

# ------------------- BusinessSocial -------------------
class BusinessSocial(Base):
    __tablename__ = "business_socials"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("business.id", ondelete="CASCADE"))
    platform = Column(SAEnum(SocialPlatform), nullable=False)
    handle = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    businesses = relationship("Business", back_populates="socials")
