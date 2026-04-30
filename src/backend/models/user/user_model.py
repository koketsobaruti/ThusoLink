# src/backend/models/user_model.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from ...database.connection import Base
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from ..business.business_model import Business

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    # Relationships
    # # User model
    businesses = relationship("Business", back_populates="owner")
    # business_bookings = relationship("BusinessBooking", back_populates="user", cascade="all, delete-orphan")
    # service_bookings = relationship("ServiceBooking", back_populates="user", cascade="all, delete-orphan")


