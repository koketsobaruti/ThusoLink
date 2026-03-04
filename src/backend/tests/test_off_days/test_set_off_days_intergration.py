import uuid
from ...modules.business.schedule_manager import ScheduleManager
from ...database.connection import get_db
from ...schemas.business.schedule_schema import AvailabilityType, SetOffDay
import pytest
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ...utils.custom_exceptions import database_exception
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import MagicMock
db_gen = get_db()
db = next(db_gen)

class BookingsTest:
    record_id:str
    column_name:str
    vals:list

@pytest.fixture(scope="module")
def setup_db():
    try:
        db_gen = get_db()
        db = next(db_gen)
        yield db
        db.close()
    except Exception as e:
        print(f"Error setting up database: {e}")

def test_set_off_day(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established")
    schedule_manager = ScheduleManager(db=setup_db)
    request = SetOffDay(record_id="31dfeee6-c543-4ad9-92cb-b57226c99c54",
                        request_type="service",
                        off_dates=["2026-03-15"])
    print(f"request sent: {request}")
    response = schedule_manager.set_off_day(request, "5650122d-e6d7-4a51-b79b-b14b804e28e6")
    assert response.status == 200
    assert response.message == "Off days set successfully"
    assert response.data["record_id"] == request.record_id

def test_set_off_day_ownership_failure(setup_db):
    schedule_manager = ScheduleManager(db=setup_db)

    request = SetOffDay(
        record_id=uuid.uuid4(),
        request_type="business",
        off_dates=["2026-03-10"]
    )

    # Mock the ownership check to fail
    schedule_manager.availability_check_map[AvailabilityType.BUSINESS] = MagicMock(
        side_effect=HTTPException(status_code=403, detail="User does not own this business")
    )

    # Expect HTTPException to propagate
    with pytest.raises(HTTPException) as exc:
        schedule_manager.set_off_day(request, "user-id")

    assert exc.value.status_code == 403
    assert exc.value.detail == "User does not own this business"

# -------------------------------
# 2️⃣ Test HTTPException from DB failure
# -------------------------------
def test_set_off_day_db_failure(setup_db):
    schedule_manager = ScheduleManager(db=setup_db)

    request = SetOffDay(
        record_id=uuid.uuid4(),
        request_type="business",
        off_dates=["2026-03-10"]
    )

    # Mock ownership check to succeed
    schedule_manager.availability_check_map[AvailabilityType.BUSINESS] = MagicMock(return_value=True)

    # Mock DB save to fail
    schedule_manager.availability_db_utils.db.execute = MagicMock(
    side_effect=SQLAlchemyError("DB is down"))

    
    with pytest.raises(database_exception.DatabaseError) as exc:
        schedule_manager.availability_db_utils.save_off_days(request)


# -------------------------------
# 3️⃣ Test missing input (HTTP 400)
# -------------------------------
def test_set_off_day_missing_input(setup_db):
    schedule_manager = ScheduleManager(db=setup_db)

    # Pass None as request to simulate missing input
    with pytest.raises(HTTPException) as exc:
        schedule_manager.set_off_day(None, "user-id")

    assert exc.value.status_code == 400
    assert exc.value.detail == "Missing input"
# from unittest.mock import MagicMock, patch
# from uuid import uuid4
# from datetime import date

# def test_set_off_day_success():

#     # Arrange
#     request = SetOffDay(
#         record_id=uuid4(),
#         request_type="business",
#         off_dates=["2026-03-10"]
#     )
#     assert response.status == 200
#     assert response.message == "Off days set successfully"
#     assert response.data["record_id"] == request.record_id