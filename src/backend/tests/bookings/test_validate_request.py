import uuid
from fastapi.testclient import TestClient
import pytest
from ...utils.availability_utils import validate_request

user_id = uuid.UUID()
def test_set_off_day_valid_request():
    off_day_request = {
    "record_id": uuid.UUID("550e8400-e29b-41d4-a716-446655440000"),
    "request_type": "business",
    "off_dates": ["2026-03-01", "2026-03-02"]}

    actual = validate_request(request=off_day_request, user_id=user_id)
    assert actual == True

def test_invaild_UUID_value():
    off_day_request = {"record_id": "not-a-uuid",
                       "request_type": "OFF",
                       "off_dates": ["2026-03-01"]}
    with pytest.raises(ValueError) as exec_info:
        validate_request(request=off_day_request, user_id=user_id)
    assert "Invalid availability type requested" in str(exec_info.detail)