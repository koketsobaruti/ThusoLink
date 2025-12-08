import datetime
from fastapi import HTTPException, status
from backend.models.business.service_model import BusinessService
from backend.schemas.business.service_schema import BusinessServiceCreate
from backend.schemas.general_response import GeneralResponse
from backend.utils.database.business_db_utils import BusinessDBUtils
from sqlalchemy.orm import Session
class ServiceManager:
    def __init__(self, db: Session):
        self.db = db
        self.bus_db_utils = BusinessDBUtils(self.db)

    def create_service(self, service_data:BusinessServiceCreate):
        try: # check if business exists
            self.bus_db_utils.business_exists(service_data.business_name)
            # get business_id_by_name 
            business_id = self.bus_db_utils.get_business_id(service_data.business_name)
            # create service logic here
            now = datetime.now(datetime.timezone.utc)
            new_service = BusinessService(
                business_id=business_id,
                name=service_data.name,
                description=service_data.description,
                price=service_data.price,
                currency=service_data.currency,
                created_at=now,
                updated_at=now
            )

            self.db.add(new_service)
            self.db.commit()
            self.db.refresh(new_service)
            return GeneralResponse(status=status.HTTP_201_CREATED,
                                    message="User registered successfully"
                                    )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )