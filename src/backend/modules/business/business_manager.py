from ...utils.database.business_db_utils import BusinessDBUtils
from sqlalchemy.orm import Session
# import GeneralResponse schema
from ...schemas.general_response import GeneralResponse
class BusinessManager:
    def __init__(self, db: Session):
        self.db = db
        self.db_utils = BusinessDBUtils(self.db)

    def get_business_by_name(self, name: str):
        
        business = self.db_utils.get_business_by_name(name)
        return GeneralResponse( 
            status= 200, 
            message="Business retrieved successfully",
            data= business
            )
    
    def get_businesses_by_user(self, user_id: int):
        businesses = self.db_utils.get_businesses_by_user(user_id)
        return GeneralResponse( 
            status= 200, 
            message="User businesses retrieved successfully",
            data= {"businesses": businesses}
            )