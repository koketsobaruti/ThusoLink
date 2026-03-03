import uuid
from ...modules.business.schedule_manager import ScheduleManager
from ...database.connection import get_db
from ...schemas.business.schedule_schema import AvailabilityType, SetOffDay
import pytest
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
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