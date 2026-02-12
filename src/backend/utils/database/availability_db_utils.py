from uuid import UUID
from ...utils.logger_utils import LoggerUtils
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ...models.business.schedule_model import Availability
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, select, and_
logger = LoggerUtils.get_logger("Availability DB Utils")
class AvailabilityDBUtils:
    def __init__(self, db: Session):
        self.db = db
    
    def save_availability(self, results):
        try:
            if not results.get("batch_data"):
                return 
            logger.info(f"Batch Data: {results.get('batch_data')}")

            query = f"""
            INSERT INTO availability
            (schedule_id, record_id, date, start_time, end_time, availability_status, availabiliity_type)
            VALUES (:schedule_id,:record_id, :date, :start_time, :end_time, :availability_status, :availabiliity_type)
            ON CONFLICT (record_id, date, start_time, end_time, availabiliity_type) DO NOTHING
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
        except Exception as e:
            logger.error(f"Unexpected error while saving availability: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while saving availability: {e}",
            )