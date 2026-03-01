from fastapi import HTTPException
import pytest
from ...database.connection import get_db
from ...utils.database.db_utils import DBUtils

@pytest.fixture(scope="module")
def setup_db():
    try:
        db_gen = get_db()
        db = next(db_gen)
        yield db
        db.close()
    except Exception as e:
        print(f"Error setting up database: {e}")

def test_verify_business_ownership_valid_input(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    db_utils = DBUtils(db = setup_db)
    owner = db_utils.user_business_exists(business_id = "7a74a6af-cbda-46cd-90e6-2ca299210b67",
                                           user_id = "5650122d-e6d7-4a51-b79b-b14b804e28e6")
    assert owner == True

def test_verify_service_ownership_wrong_business_id(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    db_utils = DBUtils(db = setup_db)
    owner = db_utils.user_business_exists(business_id = "51dfeee6-c543-4ad9-92cb-b57226c99c54", 
                                                       user_id = "7a74a6af-cbda-46cd-90e6-2ca299210b67")
    assert owner == False 

def test_verify_business_ownership_wrong_user_id(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    db_utils = DBUtils(db = setup_db)
    owner = db_utils.user_business_exists(business_id = "5650122d-e6d7-4a51-b79b-b14b804e28e6", 
                                                      user_id = "4650122d-e6d7-4a51-b79b-b14b804e28e6")
    assert owner == False

def test_verify_ownership_non_existing_business(setup_db):
    if not setup_db:
        pytest.skip("Database connection could not be established.")
    db_utils = DBUtils(db = setup_db)
    owner = db_utils.user_business_exists(business_id = "61dfeee6-c543-4ad9-92cb-b57226c99c54", 
                                                      user_id = "4650122d-e6d7-4a51-b79b-b14b804e28e6")
    assert owner == False
