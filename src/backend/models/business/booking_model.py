import uuid
from sqlalchemy import Column,DateTime, String, Date, Time, Enum as SQLEnum, ForeignKey, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ...schemas.business.bookings_schema import BookingStatus, BookingType
from ...database.connection import Base
from ...schemas.business.schedule_schema import AvailabilityStatus

class ServiceBooking(Base):
    __tablename__ = "service_booking"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    availability_id = Column(UUID(as_uuid=True), ForeignKey("service_availability.id", ondelete="CASCADE"), nullable=False)  # can join dynamically
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customization = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    # inspiration_images = Column(Text, nullable=True)  # JSON string of URLs
    status = Column(SQLEnum(BookingStatus, name="booking_status_enum"), default=BookingStatus.REQUESTED)

    booking_availability = relationship("ServiceAvailability", back_populates="bookings")  # generic relationship; for joins dynamically, use the model
    user = relationship("User", back_populates = "service_bookings")
    
class BusinessBooking(Base):
    __tablename__ = "business_booking"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    availability_id = Column(UUID(as_uuid=True), ForeignKey("business_availability.id", ondelete="CASCADE"), nullable=False)  # can join dynamically
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customization = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    # inspiration_images = Column(Text, nullable=True)  # JSON string of URLs
    status = Column(SQLEnum(BookingStatus, name="booking_status_enum"), default=BookingStatus.REQUESTED)

    # booking_availability = relationship("BusinessAvailability", back_populates="bookings")  # generic relationship; for joins dynamically, use the model
    # user = relationship("User", back_populates="business_bookings")


class Booking(Base):
    __tablename__ = "booking"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    availability_id = Column(UUID(as_uuid=True), nullable=False)  # can join dynamically
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customization = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    # inspiration_images = Column(Text, nullable=True)  # JSON string of URLs
    booking_status = Column(SQLEnum(AvailabilityStatus, name="booking_enum"), default=AvailabilityStatus.REQUESTED)
    booking_type = Column(SQLEnum(BookingType, name="booking_type_enum"), nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),  
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )