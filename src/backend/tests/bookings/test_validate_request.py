import uuid
from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from ...utils.availability_utils import validate_request
from ...schemas.business.schedule_schema import SetOffDay
user_id = uuid.uuid4() 
def test_set_off_day_valid_request():
    off_day_request = SetOffDay(record_id = uuid.uuid4(),
                                request_type = "business",
                                off_dates = ["2026-03-01", "2026-03-02"])

    validate_request(off_day_request, uuid.uuid4())

def test_invaild_UUID_record_value():
    off_day_request = SetOffDay(record_id= "",
                       request_type = "OFF",
                       off_dates= ["2026-03-01"])
    with pytest.raises(ValueError, match="A valid record ID must be provided") as exec_info:
        validate_request(request=off_day_request, user_id=uuid.uuid4())
    # assert "Record ID must be provided" in str(exec_info.detail)