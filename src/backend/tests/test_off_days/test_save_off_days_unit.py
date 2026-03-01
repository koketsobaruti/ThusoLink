from uuid import uuid4

from fastapi import HTTPException
import pytest
from ...database.connection import get_db
from ...utils.database.availability_db_utils import AvailabilityDBUtils
from ...schemas.business.schedule_schema import SetOffDay
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

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

def test_sqlalchemy_error(mock_db):
    mock_db.execute.side_effect = SQLAlchemyError("DB failure")
    request = SetOffDay(record_id=uuid4(),
                        request_type="business",
                        off_dates=["2026-03-14"])
    db_utils = AvailabilityDBUtils(db=mock_db)
    with pytest.raises(Exception) as exc:
        db_utils.save_off_days(request)
    print(type(exc.value))
    print(exc.value)
    assert exc.value.status_code == 500
    assert mock_db.rollback.called
    assert not mock_db.commit.called
# these functions worked well. They did not save invalid inputs because the SetOffDay does not let it go that far
# def test_save_empty_days(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     request = SetOffDay(record_id=uuid4(),
#                         request_type="business",
#                         off_dates=[])
#     db_utils = AvailabilityDBUtils(db=setup_db)
#     with pytest.raises(ValidationError):
#         db_utils.save_off_days(request) 

# def test_save_duplicate_days(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     db_utils = AvailabilityDBUtils(db=setup_db)
#     with pytest.raises(ValidationError):
#         SetOffDay(record_id=uuid4(),
#                         request_type="service",
#                         off_dates=["2026-03-10", "2026-03-14", "2026-03-14"])

# def test_invalid_request_type(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     request = SetOffDay(record_id=uuid4(),
#                         request_type="off",
#                         off_dates=["2026-04-19"])
#     db_utils = AvailabilityDBUtils(db=setup_db)
#     with pytest.raises(ValidationError):
#         db_utils.save_off_days(request) 


# def test_invalid_record_id(setup_db):
#     if not setup_db:
#         pytest.skip("Database connection could not be established.")
#     request = SetOffDay(record_id="not-a-uuid",
#                         request_type="off",
#                         off_dates=["2026-04-20"])
#     db_utils = AvailabilityDBUtils(db=setup_db)
#     with pytest.raises(ValidationError):
#         db_utils.save_off_days(request) 
