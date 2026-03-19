import uuid

from ...utils.database.booking_db_utils import BookingDBUtils
from ...database.connection import get_db
import pytest
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from ...schemas.business.bookings_schema import GetBooking
from ...schemas.business.bookings_schema import UpdateBookings
from ...schemas.business.bookings_schema import BookingStatus

@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture(scope="module")
def setup_db():
    try:
        db_gen = get_db()
        db = next(db_gen)
        yield db
        db.close()
    except Exception as e:
        print(f"Error setting up database: {e}")
        
def test_update_booking_status_valid():
    # Arrange
    update_bookings_obj = UpdateBookings(booking_id=[uuid.UUID("fa97be97-1f81-4753-a99a-1b82477e34b4")],
                                         status_value=BookingStatus.RESCHEDULE_REQUIRED)

    actual_status = update_bookings_obj.status_value
    print(BookingStatus.RESCHEDULE_REQUIRED.value)
    assert actual_status == BookingStatus.RESCHEDULE_REQUIRED.value
# def test_update_booking_status_valid():
