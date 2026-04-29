import uuid

from fastapi import HTTPException
import pytest
from ...database.connection import get_db
from ...utils.database.db_utils import DBUtils
from unittest import mock
from ...models.user.user_model import User
from datetime import datetime, timezone

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
    actual = db_utils.email_exists("fakemeail@example.com")
