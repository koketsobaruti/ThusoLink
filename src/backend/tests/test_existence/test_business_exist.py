from fastapi import HTTPException
import pytest
from ...database.connection import get_db
from ...utils.database.service_db_utils import ServiceDBUtils

@pytest.fixture(scope="module")
def setup_db():
    try:
        db_gen = get_db()
        db = next(db_gen)
        yield db
        db.close()
    except Exception as e:
        print(f"Error setting up database: {e}")
    