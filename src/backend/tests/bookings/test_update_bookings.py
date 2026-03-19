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

@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

def test_update_booking_status_valid():
    # Arrange
    update_bookings_obj = UpdateBookings(booking_id=[uuid.uuid4()],
                                         status_value=BookingStatus.RESCHEDULE_REQUIRED)
    actual_status = update_bookings_obj.status_value
    print(BookingStatus.RESCHEDULE_REQUIRED.value)
    assert actual_status == BookingStatus.RESCHEDULE_REQUIRED.value

def test_invalid_id():
    with pytest.raises(ValueError, match="UUID"):
        UpdateBookings(booking_id=["not-uuid"],
                       status_value=BookingStatus.RESCHEDULE_REQUIRED)
def test_invalid_booking_status():
    with pytest.raises(ValueError):
        UpdateBookings(
            booking_id=[uuid.uuid4()],
            status_value="invalid_status"
        )
def test_missing_id():
    with pytest.raises(ValueError):
        UpdateBookings(booking_id=[],
                       status_value=BookingStatus.RESCHEDULE_REQUIRED)
        
def test_missing_inputs():
    with pytest.raises(ValueError):
        UpdateBookings(booking_id=[],
                       status_value="")
        

def test_update_booking_db_valid(mock_db):
    booking_db_utils = BookingDBUtils(db=mock_db)
    update_bookings_obj = UpdateBookings(booking_id=[uuid.UUID("fa97be97-1f81-4753-a99a-1b82477e34b4")],
                                         status_value=BookingStatus.RESCHEDULE_REQUIRED)
    booking_db_utils.update_booking_status(update_bookings_obj)
    args, kwargs = mock_db.execute.call_args
    assert "UPDATE booking" in str(args[0])  # query string
    params = args[1]  # the dict with 'status' and 'booking_ids'

    assert params["booking_status"] == BookingStatus.RESCHEDULE_REQUIRED
    assert params["booking_ids"] == [uuid.UUID("fa97be97-1f81-4753-a99a-1b82477e34b4")]

    # 2️⃣ Commit called
    mock_db.commit.assert_called_once()

    # 3️⃣ Rollback not called
    mock_db.rollback.assert_not_called()

def test_update_using_actual_db(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    booking_db_utils = BookingDBUtils(db=setup_db)
    booking_id = uuid.UUID("30cadfdf-1828-4084-a82a-2b16481bbac2")
    update_obj = UpdateBookings(booking_id=[booking_id],
                                status_value=BookingStatus.RESCHEDULE_REQUIRED.value)
    with setup_db.begin_nested():
        booking_db_utils.update_booking_status(update_obj)

        result = setup_db.execute(
            "SELECT booking_status FROM booking WHERE id=:id",
            {"id":booking_id}).fetchone()
        
        assert result.booking_status == BookingStatus.RESCHEDULE_REQUIRED.value

