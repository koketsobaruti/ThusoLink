import datetime
from fastapi import HTTPException, status
from ...models.business.service_model import BusinessService
from ...schemas.business.service_schema import BusinessServiceCreate, BusinessServiceListResponse, BusinessServiceResponse
from ...schemas.general_response import GeneralResponse
from ...utils.database.business_db_utils import BusinessDBUtils
from ...utils.database.service_db_utils import ServiceDBUtils
from sqlalchemy.orm import Session
from ...utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Service Manager")
class ServiceManager:
    def __init__(self, db: Session):
        self.db = db
        self.bus_db_utils = BusinessDBUtils(self.db)

    def view_all_services(self, business_name: str) -> list[BusinessService]:
        try:
            self.bus_db_utils.get_business(business_name)
            business_id = self.bus_db_utils.get_business_id(business_name)
            services = self.db.query(BusinessService).filter(BusinessService.business_id == business_id).all()
            
            services_dict = [BusinessServiceResponse.model_validate(p) for p in services]
            logger.info(f"List of services {services_dict}")
            return GeneralResponse(
                status=status.HTTP_200_OK,
                message="Services retrieved successfully",
                data={"services": services_dict} 
            )
        
        except HTTPException as e:
            self.db.rollback()
            logger.error(f"Error getting all services for business {business_name}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        