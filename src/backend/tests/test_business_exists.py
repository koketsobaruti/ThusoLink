from fastapi import HTTPException

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
    
def test_verify_service_ownership_valid_input(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    service_db_utils = ServiceDBUtils(db = setup_db)
    owner = service_db_utils.verify_service_ownership(service_id = "31dfeee6-c543-4ad9-92cb-b57226c99c54", 
                                                      user_id = "5650122d-e6d7-4a51-b79b-b14b804e28e6")
    assert owner == True

def test_verify_service_ownership_wrong_service_id(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    service_db_utils = ServiceDBUtils(db = setup_db)
    with pytest.raises(HTTPException):
        owner = service_db_utils.verify_service_ownership(service_id = "51dfeee6-c543-4ad9-92cb-b57226c99c54", 
                                                      user_id = "5650122d-e6d7-4a51-b79b-b14b804e28e6")
    assert owner == False 