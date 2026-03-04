import uuid

from ...utils.database.booking_db_utils import BookingDBUtils
from ...database.connection import get_db
import pytest
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

class BookingsTest:
    record_id:str
    column_name:str
    vals:list

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
        
def test_get_bookings_with_all_values(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    booking_db_utils = BookingDBUtils(db=setup_db)
    actual = booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
                                           column_name="date",
                                           vals=["2026-02-12"])
    print(f"Actual: {actual}")
    expected = [{"id":uuid.UUID("30cadfdf-1828-4084-a82a-2b16481bbac2"),
                "availability_id":uuid.UUID("aa6c4d3d-6895-4654-8e4d-2f4a50371856"),
                "customer_id":uuid.UUID("5650122d-e6d7-4a51-b79b-b14b804e28e6"),
                "customization":"Standard haircut",
                "notes":"Customer prefers morning appointment",
                "booking_type":"BUSINESS"}]
    assert actual == expected

def test_get_bookings_with_none_record_id(mock_db):
    booking_db_utils = BookingDBUtils(db=mock_db)
    with pytest.raises(HTTPException) as exc_info:
        booking_db_utils.get_bookings(record_id=None,
                                      column_name="date",
                                      vals=["2026-02-12"])
    assert exc_info.value.detail  == "Missing input"
    
def test_get_bookings_with_none_column_name(mock_db):
    booking_db_utils = BookingDBUtils(db=mock_db)
    with pytest.raises(HTTPException) as exc_info:
        booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
                                      column_name=None,
                                      vals=["2026-02-12"])
    assert exc_info.value.detail == "Missing input"

def test_get_bookings_with_none_vals(mock_db):
    booking_db_utils = BookingDBUtils(db=mock_db)
    with pytest.raises(HTTPException) as exc_info:
        booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
                                      column_name="date",
                                      vals=[])
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Missing input"

# def test_get_bookings_with_invalid_record_id(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     booking_db_utils = BookingDBUtils(db=setup_db)
#     with pytest.raises(HTTPException) as exc_info:
#         booking_db_utils.get_bookings(record_id="invalid_record_id",
#                                       column_name="date",
#                                       vals=["2026-02-12"])
#     assert exc_info.value.status_code == 500
#     assert exc_info.value.detail == "Internal server error" in str(exc_info.value.detail)

# def test_get_bookings_with_invalid_column_name(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     booking_db_utils = BookingDBUtils(db=setup_db)
#     with pytest.raises(HTTPException) as exc_info:
#         booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
#                                       column_name="invalid_column",
#                                       vals=["2026-02-12"])
#     assert exc_info.value.status_code == 500
#     assert exc_info.value.detail == "Internal server error" in str(exc_info.value.detail)

# def test_get_bookings_with_invalid_vals(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     booking_db_utils = BookingDBUtils(db=setup_db)
#     with pytest.raises(HTTPException) as exc_info:
#         booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
#                                       column_name="date",
#                                       vals=["invalid_date"])
#     assert exc_info.value.status_code == 500
#     assert exc_info.value.detail == "Internal server error" in str(exc_info.value.detail)



# def test_get_bookings_with_empty_vals(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     booking_db_utils = BookingDBUtils(db=setup_db)
#     with pytest.raises(HTTPException) as exc_info:
#         booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
#                                       column_name="date",
#                                       vals=[])
#     assert exc_info.value.status_code == 500
#     assert exc_info.value.detail == "Internal server error" in str(exc_info.value.detail)

# def test_get_bookings_with_invalid_column_name(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     booking_db_utils = BookingDBUtils(db=setup_db)
#     with pytest.raises(HTTPException) as exc_info:
#         booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
#                                       column_name="invalid_column",
#                                       vals=["2026-02-12"])
#     assert exc_info.value.status_code == 500
#     assert exc_info.value.detail == "Internal server error" in str(exc_info.value.detail)


# def test_get_bookings_with_no_record_id_entry(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     booking_db_utils = BookingDBUtils(db=setup_db)
#     with pytest.raises(HTTPException) as exc_info:
#         booking_db_utils.get_bookings(column_name="date",
#                                       vals=["2026-02-12"])
#     assert exc_info.value.status_code == 500
#     assert exc_info.value.detail == "Internal server error" in str(exc_info.value.detail)

# def test_get_bookings_with_no_column_name_entry(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     booking_db_utils = BookingDBUtils(db=setup_db)
#     with pytest.raises(HTTPException) as exc_info:
#         booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
#                                       vals=["2026-02-12"])
#     assert exc_info.value.status_code == 500
#     assert exc_info.value.detail == "Internal server error" in str(exc_info.value.detail)

# def test_get_bookings_with_no_vals_entry(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    booking_db_utils = BookingDBUtils(db=setup_db)
    with pytest.raises(HTTPException) as exc_info:
        booking_db_utils.get_bookings(record_id="7a74a6af-cbda-46cd-90e6-2ca299210b67",
                                      column_name="date")
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal server error" in str(exc_info.value.detail)