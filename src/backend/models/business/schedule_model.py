# create the sqlalchemy models for schedule
from sqlalchemy import Enum
import uuid
from sqlalchemy import (Column, Integer, ForeignKey, Date, Time, CheckConstraint, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID     
from sqlalchemy.orm import relationship
from ...database.connection import Base
from ...schemas.business.schedule_schema import AvailabilityStatus
from ...schemas.business.bookings_schema import BookingStatus, BookingType
class Availability(Base):
    __tablename__ = "availability"
    __table_args__ = (
        CheckConstraint("end_time >= start_time", name="ck_valid_time_range"),
        UniqueConstraint('record_id', 'date', 'start_time', 'end_time', name='uq_record_date'),
        {"extend_existing": True},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id = Column(UUID(as_uuid=True), nullable=False)  # can join dynamically
    date = Column(Date, nullable=False)
    start_time = Column(Time(timezone=True), nullable=False)
    end_time = Column(Time(timezone=True), nullable=False)

    availability_status = Column(
        Enum(AvailabilityStatus, name="availability_enum"),
        nullable=False,
        default=AvailabilityStatus.AVAILABLE
    )
    availabiliity_type = Column(Enum(BookingType, name = "availability_type_enum"), nullable=False)

class ServiceAvailability(Base):
    __tablename__ = "service_availability"
    __table_args__ = (
            CheckConstraint("end_time >= start_time", name="ck_business_valid_time_range"),
            UniqueConstraint('service_id', 'date', 'start_time', 'end_time', name='uq_service_date'),
            {"extend_existing": True},
        )
    
    fk_field = "service_id"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id = Column(UUID(as_uuid=True), ForeignKey("business_services.id", ondelete="CASCADE"), nullable=False)


    date = Column(Date, nullable=False)
    start_time = Column(Time(timezone=True), nullable=False)
    end_time = Column(Time(timezone=True), nullable=False)

    availability_status = Column(
        Enum(AvailabilityStatus, name="availability_status_enum"),
        nullable=False,
        default=AvailabilityStatus.AVAILABLE
    )
    service = relationship("BusinessService", back_populates="availability")
    bookings = relationship("ServiceBooking", back_populates="booking_availability", cascade="all, delete-orphan")


class BusinessAvailability(Base):
    __tablename__ = "business_availability"
    __table_args__ = (
        CheckConstraint("end_time >= start_time", name="ck_business_valid_time_range"),
        UniqueConstraint('business_id', 'date', 'start_time', 'end_time', name='uq_business_date'),
        {"extend_existing": True},
    )
    fk_field = "business_id"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    business_id = Column(UUID(as_uuid=True),
        ForeignKey("business.id", ondelete="CASCADE"),
        nullable=False
    )

    date = Column(Date, nullable=False)
    start_time = Column(Time(timezone=True), nullable=False)
    end_time = Column(Time(timezone=True), nullable=False)

    availability_status = Column(
        Enum(AvailabilityStatus, name="availability_status_enum"),
        nullable=False,
        default=AvailabilityStatus.AVAILABLE
    )

    business = relationship("Business", back_populates="availability")
    bookings = relationship("BusinessBooking", back_populates="booking_availability", cascade="all, delete-orphan")

# class StaffAvailability(Base):
#     __tablename__ = "staff_availability"
#     __table_args__ = (
#         CheckConstraint("end_time >= start_time", name="ck_staff_valid_time_range"),
#         UniqueConstraint("staff_id", "date", "start_time", "end_time", name="uq_staff_date"),
#     )

#     fk_field = "staff_id"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     staff_id = Column(UUID(as_uuid=True), nullable=False)
#     date = Column(Date, nullable=False)
#     start_time = Column(Time(timezone=True), nullable=False)
#     end_time = Column(Time(timezone=True), nullable=False)
#     availability_status = Column(Enum(AvailabilityStatus, name="availability_status_enum"),
#             nullable=False,
#             default=AvailabilityStatus.AVAILABLE
#         )
    
#     # staff = relationship("Staff", back_populates="availability")
