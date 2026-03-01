import pytest
from ..database.connection import get_db
from ..utils.database.service_db_utils import ServiceDBUtils

@pytest.fixture(scope="module")
def setup_db():
    try:
        db_gen = get_db()
        db = next(db_gen)
        yield db
        db.close()
    except Exception as e:
        print(f"Error setting up database: {e}")
    
def test_get_bookings_with_all_values(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    service_db_utils = ServiceDBUtils(db = setup_db)
    owner = service_db_utils.verify_service_ownership("31dfeee6-c543-4ad9-92cb-b57226c99c54", "7a74a6af-cbda-46cd-90e6-2ca299210b67")
    assert owner == True
