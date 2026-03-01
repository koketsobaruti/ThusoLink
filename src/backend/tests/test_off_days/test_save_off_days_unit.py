from uuid import uuid4

from fastapi import HTTPException
import pytest
from ...database.connection import get_db
from ...utils.database.availability_db_utils import AvailabilityDBUtils
from ...schemas.business.schedule_schema import SetOffDay
from pydantic import ValidationError

from unittest.mock import MagicMock
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


def test_save_off_days_valid(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    request = SetOffDay(record_id=uuid4(),
                        request_type="business",
                        off_dates=["2026-03-10", "2026-03-11"])
    db_utils = AvailabilityDBUtils(db=setup_db)
    db_utils.save_off_days(request)

def test_save_off_days_one_date(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    request = SetOffDay(record_id=uuid4(),
                        request_type="service",
                        off_dates=["2026-04-10"])
    db_utils = AvailabilityDBUtils(db=setup_db)
    db_utils.save_off_days(request) 

def test_save_duplicate_days(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    request = SetOffDay(record_id=uuid4(),
                        request_type="service",
                        off_dates=["2026-03-10", "2026-03-14", "2026-03-14"])
    db_utils = AvailabilityDBUtils(db=setup_db)
    with pytest.raises(ValidationError):
        db_utils.save_off_days(request) 

def test_save_empty_days(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    request = SetOffDay(record_id=uuid4(),
                        request_type="business",
                        off_dates=[])
    db_utils = AvailabilityDBUtils(db=setup_db)
    with pytest.raises(ValidationError):
        db_utils.save_off_days(request) 

def test_sqlalchemy_error(mock_db):
    request = SetOffDay(record_id=uuid4(),
                        request_type="business",
                        off_dates=["2026-03-14"])
    db_utils = AvailabilityDBUtils(db=mock_db)
    db_utils.save_off_days(request) 

    assert mock_db.execute.called
    assert mock_db.commit.called

def test_invalid_request_type(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    request = SetOffDay(record_id=uuid4(),
                        request_type="off",
                        off_dates=["2026-04-19"])
    db_utils = AvailabilityDBUtils(db=setup_db)
    with pytest.raises(ValidationError):
        db_utils.save_off_days(request) 

def test_invalid_record_id(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    request = SetOffDay(record_id="not-a-uuid",
                        request_type="off",
                        off_dates=["2026-04-20"])
    db_utils = AvailabilityDBUtils(db=setup_db)
    with pytest.raises(ValidationError):
        db_utils.save_off_days(request) 
