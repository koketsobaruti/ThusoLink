from unittest.mock import MagicMock
import uuid
from ...app import app
from fastapi.testclient import TestClient
from ..database.connection import get_db
from ..auth.jwt_bearer import get_current_user
import pytest
def override_get_db():
    return MagicMock()

@pytest.fixture
def client():

    def override_get_db():
        return MagicMock()

    def override_get_current_user():
        class FakeUser:
            id = uuid.UUID()
        return FakeUser()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides = {}

@pytest.fixture()
def setup_db():
    try:
        db_gen = get_db()
        db = next(db_gen)
        yield db
        db.close()
    except Exception as e:
        print(f"Error setting up database: {e}")
        