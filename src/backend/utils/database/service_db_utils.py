from click import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Union
from ...utils.logger_utils import LoggerUtils
from ...models.business.service_model import BusinessService
from ...schemas.business.schedule_schema import AvailabilityFilter
from ...models.business.business_model import Business
from sqlalchemy.exc import SQLAlchemyError
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy import text, select, and_

logger = LoggerUtils.get_logger("Service DB Utils")
class ServiceDBUtils:
    def __init__(self, db: Session):
        self.db = db

    def get_service_by_id(self, service_id: int) -> Union[dict, None]:
        try:
            service = self.db.execute(
                "SELECT * FROM services WHERE id = :service_id",
                {"service_id": service_id}
            ).fetchone()
            if not service:
                raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail="No service found for the service: {id}."
                )
            return dict(service)
            
        except Exception as e:
            logger.error(f"Error fetching service by ID {service_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while fetching service.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
    def get_all_availability(self, table_name, id, id_column_name):
        try:
            query = text(f"""SELECT * FROM {table_name} WHERE {id_column_name}=:id_value""")
            all_availability = self.db.execute( query, {"id_value": id}).fetchall()
            logger.info(f"All Availability: {all_availability}")
            if not all_availability:
                raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail="No availability  found for the businesses: {id}."
                )

            return [dict(row._mapping) for row in all_availability] if all_availability else []

        except Exception as e:
            logger.error(f"Error fetching item: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error while fetching availability for {table_name}.",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    def get_availability_by_filter(self, model, id_column, filters: AvailabilityFilter):
        try:
            stmt = select(model)
            conditions = []

             # Dynamic record_id filter
            if id_column and filters.record_id:
                conditions.append(getattr(model, id_column) == filters.record_id)

            # Common filters
            if filters.selected_date:
                conditions.append(getattr(model, "date") == filters.selected_date)
            if filters.start_time:
                conditions.append(getattr(model, "start_time") >= filters.start_time)
            if filters.end_time:
                conditions.append(getattr(model, "end_time") <= filters.end_time)
            if filters.availability_status:
                conditions.append(getattr(model, "availability_status") == filters.availability_status)

            if conditions:
                stmt = stmt.where(and_(*conditions))

            results = self.db.execute(stmt).scalars().all()
            return results

        except Exception as e:
            logger.error(f"Error fetching data based on filters: {e}")
            raise
        
        
    def verify_service_ownership(self, service_id, user_id) -> bool:
        try:
            service = (self.db.query(BusinessService).join(Business).filter(BusinessService.id == service_id,
                                                                    Business.owner_id == user_id).first())
            if not service:
                logger.warning(f"Ownership verification failed for service ID {service_id} and user ID {user_id}")
                return False
            return True
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while verifying service ownership.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
    def save_availability(self, results, table_name: str, id_column: str, column_name:str) -> None:
        
        if not results.get("batch_data"):
            return 
        logger.info(f"Batch Data: {results.get("batch_data")}")
        id = UUID(id_column)

        # query = f"""
        #     INSERT INTO {table_name}
        #     (id, {column_name}, date, start_time, end_time, availability_status)
        #     VALUES (:schedule_id, :id, :date, :start_time, :end_time, :availability_status)
        # """
        query = f"""
        INSERT INTO {table_name}
        (id, {column_name}, date, start_time, end_time, availability_status)
        VALUES (:schedule_id, :id, :date, :start_time, :end_time, :availability_status)
        ON CONFLICT ({column_name}, date, start_time, end_time) DO NOTHING
        """

        try:

            self.db.execute(text(query), results["batch_data"])
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to persist availability slots : {e}.",
            )

        output = {
            "inserted_count": len(results["valid_slots"]),
            "failed_count": len(results["failed"]),
            "inserted": results["valid_slots"],
            "failed": results["failed"],
        }
        logger.info(output)
