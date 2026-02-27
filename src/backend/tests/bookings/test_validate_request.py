import uuid
from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from ...utils.availability_utils import validate_request
from ...schemas.business.schedule_schema import SetOffDay
test_user_id=uuid.uuid4()
test_record_id=uuid.uuid4()
def test_set_off_day_valid_request():
    off_day_request = SetOffDay(record_id = test_record_id,
    request_type= "business",
    off_dates = ["2026-03-01", "2026-03-02"])
    validate_request(request=off_day_request, user_id=test_user_id)

def test_no_off_days():
    off_day_request = SetOffDay(record_id= test_record_id,
                                request_type= "business",
                                off_dates = [])

    with pytest.raises(ValueError, match ="At least one off date must be provided"):
        validate_request(request=off_day_request, user_id=test_user_id)

def test_invalid_date_before_today():
    off_day_request = SetOffDay(record_id= test_record_id,
                                request_type= "business",
                                off_dates = ["2026-02-20"])
    with pytest.raises(ValueError, match ="Off dates cannot be in the past"):
        validate_request(request=off_day_request, user_id=test_user_id)

def test_invalid_request_type():
    off_day_request = SetOffDay(record_id= test_record_id,
                                request_type= "off",
                                off_dates = ["2026-02-29"])
    with pytest.raises(HTTPException):
        validate_request(request=off_day_request, user_id=test_user_id)