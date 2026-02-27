import uuid
from fastapi.testclient import TestClient
import pytest
from ...routes.booking import validate_request

def test_set_off_day_valid_request():
    off_day_request = {
    "record_id": uuid.UUID("550e8400-e29b-41d4-a716-446655440000"),
    "request_type": "business",
    "off_dates": ["2026-03-01", "2026-03-02"]}
    actual = validate_request(off_day_request)
    assert actual == True

def test_invaild_UUID_value():
    off_day_request = {"record_id": "not-a-uuid",
                       "request_type": "OFF",
                       "off_dates": ["2026-03-01"]}
    with pytest.raises(ValueError) as exec_info:
        validate_request(off_day_request)
    assert "Invalid availability type requested" in str(exec_info.detail)