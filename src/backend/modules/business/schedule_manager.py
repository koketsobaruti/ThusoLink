from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
from uuid import uuid4
from fastapi import HTTPException, status
from ...models.business.service_model import BusinessService
from ...schemas.business.service_schema import BusinessServiceCreate, BusinessServiceListResponse, BusinessServiceResponse
from ...schemas.general_response import GeneralResponse
from ...utils.database.db_utils import DBUtils
from ...utils.availability_utils import check_availability_input
from ...schemas.business.schedule_schema import AvailabilityFilter, AvailabilityResponse
from ...utils.database.service_db_utils import ServiceDBUtils
from sqlalchemy.orm import Session
from ...config.availability_map import AVAILABILITY_MAP
from ...utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Schedule Manager")
class ScheduleManager:
    def __init__(self, db: Session):
        self.db = db
        self.service_db_utils = ServiceDBUtils(self.db)
        self.general_db_utils = DBUtils(self.db)

    def set_service_availability(self, service_id, owner_id, slots: list[dict]) -> GeneralResponse:
        try:
            # Verify service ownership
            self.service_db_utils.verify_service_ownership(service_id, owner_id)
            # results = self.check_availability_input(id=service_id, slots=slots)
            results = check_availability_input(id=service_id, slots=slots)
            # Here you would add logic to save the slots to the database
            self.service_db_utils.save_availability(results, "service_availability", id_column=service_id, column_name="service_id")

            return GeneralResponse(
                status=status.HTTP_200_OK,
                message="Availability slots set successfully",
                data={"service_id": service_id, "slots": slots}
            )

        except HTTPException as e:
            self.db.rollback()
            logger.error(f"Error setting availability slots for service ID {service_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )

    def set_business_availability(self, business_id, owner_id, slots: list[dict])-> GeneralResponse:
        try:
            self.general_db_utils.user_business_exists(business_id, owner_id)
            # results = self.check_availability_input(id=business_id, slots=slots)
            results = check_availability_input(id=business_id, slots=slots)
            self.service_db_utils.save_availability(results, "business_availability", id_column=business_id, column_name="business_id")
            return GeneralResponse(
                    status=status.HTTP_200_OK,
                    message="Availability slots set successfully",
                    data={"service_id": business_id, "slots": slots}
                )

        except HTTPException as e:
            self.db.rollback()
            logger.error(f"Error setting availability slots for service ID {business_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
    def get_business_availability(self, business_id) -> GeneralResponse:
        try:
            business_availabilty = self.service_db_utils.get_all_availability(table_name = "business_availability", 
                                                                                  id=business_id, 
                                                                                  id_column_name = "business_id")
        
            return GeneralResponse(
                status=status.HTTP_200_OK,
                message="Business availability aquired successfully",
                data={"business_availabilty": business_availabilty}
            )
        except Exception as e:
            logger.error(f"Error getting availabilty for business id: {business_id}")
    
    def get_service_availability(self, service_id) -> GeneralResponse:
        try:
            service_availabilty = self.service_db_utils.get_all_availability(table_name = "service_availability", 
                                                                                  id=service_id, 
                                                                                  id_column_name = "service_id")
        
            return GeneralResponse(
                status=status.HTTP_200_OK,
                message="Business availability aquired successfully",
                data={"business_availabilty": service_availabilty}
            )
        except Exception as e:
            logger.error(f"Error getting availabilty for business id: {service_id}")
    
    def get_availability_by_filter(self, filters: AvailabilityFilter):
        try:

            model, record_column = AVAILABILITY_MAP[filters.availability_type.value]

            # Fetch results from repo
            results = self.service_db_utils.get_availability_by_filter(model=model,
                                                                       id_column=record_column,
                                                                       filters=filters)

            if not results:
                return GeneralResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="No availability found for the provided filters",
                    data={"results": []}
                )

            # Optional: convert ORM objects to dicts for JSON serialization
            serialized_results = [AvailabilityResponse(id=r.id,
                                                        record_id=getattr(r, r.fk_field),  # dynamic for business_id/service_id
                                                        date=r.date,
                                                        start_time=r.start_time,
                                                        end_time=r.end_time,
                                                        availability_status=r.availability_status.value
                                                    ).dict()
                                                    for r in results]

            return GeneralResponse(
                status=status.HTTP_200_OK,
                message="Business availability acquired successfully",
                data={"results": serialized_results}
            )

        except HTTPException as he:
            # Let HTTPExceptions pass through
            raise he

        except Exception as e:
            logger.error(f"Error getting results for filters {filters}: {e}")
            return GeneralResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error while fetching availability",
                data={"results": []}
            )
    # WE HAVE MOVED THESE TO availability_utils file
    # def check_availability_input(self, id, slots):
    #     failed = []
    #     # Validate slots in parallel
    #     results = []
    #     with ThreadPoolExecutor(max_workers=5) as executor:
    #         futures = {executor.submit(self.validate_and_insert_slot, idx, slot): idx for idx, slot in enumerate(slots)}
    #         for future in as_completed(futures):
    #             results.append(future.result())
        
    #     # Batch insert validated slots
    #     valid_slots = [r for r in results if r["status"] == "success"]
    #     failed = [r for r in results if r["status"] == "failed"]
    #     logger.info(f"Valid data: {valid_slots}")
    #     if valid_slots:
    #         try:
    #             batch_data = [{
    #                 "schedule_id": uuid4(),
    #                 "id": id,
    #                 "date": r["slot"].date,
    #                 "start_time": r["slot"].start_time,
    #                 "end_time": getattr(r["slot"], "end_time", r["slot"].start_time),
    #                 "availability_status": r["slot"].availability_status.name
    #             } for r in valid_slots]
    #             results = {"batch_data":batch_data,
    #                         "failed": failed,
    #                         "valid_slots":valid_slots}
    #             return results
    #         except HTTPException as e: 
    #             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                                 detail=f"Failed to persist availability slots {e}.")

    # def validate_and_insert_slot(self, idx, slot):
    #     try:
    #         if slot.start_time > slot.end_time:
    #             logger.warning(f"Invalid slot time: start_time {slot.start_time} is after end_time {slot.end_time}")
    #             raise ValueError("Invalid slot time: start_time must be before end_time.")
    #         return {"index": idx,
    #                 "slot": slot,
    #                 "status": "success"}
    #     except (KeyError, ValueError) as e:
    #         return {"index": idx,
    #                 "slot": slot,
    #                 "status": "failed",
    #                 "reason": str(e)}
    

    