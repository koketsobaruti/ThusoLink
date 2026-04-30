import uuid

from fastapi import HTTPException
import pytest
from ...database.connection import get_db
from ...utils.database.db_utils import DBUtils
from unittest import mock
from ...models.user.user_model import User
from datetime import datetime, timezone
from ...schemas.user.user_schema import UserCreate
from ...utils.auth.hash_utils import hash_password
from sqlalchemy.exc import SQLAlchemyError
from ...modules.auth.registration_manager import RegistrationManager
@pytest.fixture()
def mock_user():
    mock = mock.MagicMock(spec=User)
    mock.id = uuid.uuid4()
    mock.email = "mock@example.com"
    mock.password = "hashedpassword"
    mock.name = "Mock User"
    mock.created_at = datetime.now(timezone.utc)
    mock.updated_at = datetime.now(timezone.utc)
    return mock

@pytest.fixture()
def mock_db():
    db = mock.MagicMock()
    return db

@pytest.fixture(scope="module")
def setup_db():
    try:
        db = next(get_db())
        yield db
    except Exception as e:
        pytest.skip(f"Database connection could not be established: {str(e)}")
    finally:
        db.close()

def test_email_exists_with_existing_email(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    db_utils = DBUtils(setup_db)
    with pytest.raises(HTTPException) as exc_info:
        db_utils.email_exists("test@example.com")
    assert exc_info.value.detail == "Email already registered."
    assert exc_info.value.status_code == 400

def test_email_exists_with_non_existing_email(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    db_utils = DBUtils(setup_db)
    assert db_utils.email_exists("none@example.com") == None

def test_email_exists_with_db_error(mock_db):
    db_utils = DBUtils(mock_db)
    mock_db.query().filter().first.side_effect = SQLAlchemyError()
    with pytest.raises(SQLAlchemyError):
        db_utils.email_exists("false@example.com")

def test_register_incorrect_details():
    with pytest.raises(ValueError) as exc_info:
        UserCreate(
            full_name="Test User",
            email="invalid-email",
            password="password123"
        )
        assert exc_info.value.errors()[0]['loc'] == ('email',)
        assert exc_info.value.errors()[0]['msg'] == 'value is not a valid email address'

def test_register_valid_details(mock_db):
    user_data = UserCreate(
        full_name="Test User",
        email="testeraccount@example.com",
        password=hash_password("password123")
    )
    registration_manager = RegistrationManager(mock_db)
    assert registration_manager.register_user(user_data) is not None