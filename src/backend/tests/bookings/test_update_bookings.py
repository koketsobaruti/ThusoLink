import uuid

from ...utils.database.booking_db_utils import BookingDBUtils
from ...database.connection import get_db
import pytest
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from ...schemas.business.bookings_schema import GetBooking

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
        

# def test_update_booking_status_valid():
