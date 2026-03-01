from collections.abc import Iterable
from datetime import datetime, timezone
from pyexpat import model
from uuid import UUID, uuid4
from ...utils.logger_utils import LoggerUtils
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ...models.business.schedule_model import Availability
from ...schemas.business.schedule_schema import AvailabilityFilter
from ...schemas.business.schedule_schema import SetOffDay

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, select, and_, bindparam
from ..database.CRUD import update
logger = LoggerUtils.get_logger("Availability DB Utils")
class AvailabilityDBUtils:
    def __init__(self, db: Session):
        self.db = db
        self.update_utils = update.UpdateUtils(db)
    def save_availability(self, results):
        try:
            if not results.get("batch_data"):
                return 
            logger.info(f"Batch Data: {results.get('batch_data')}")

            query = f"""
            INSERT INTO availability
            (id, record_id, date, start_time, end_time, availability_status, availabiliity_type, created_at, updated_at)
            VALUES (:id,:record_id, :date, :start_time, :end_time, :availability_status, :availabiliity_type, :created_at, :updated_at)
            ON CONFLICT (record_id, date, start_time, end_time) DO NOTHING
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
        
    def save_off_days(self, request:SetOffDay):
        logger.info(f"Saving off days for record_id: {request.record_id} and record: {request}")
        try:
            query = f"""INSERT INTO off_day
            (id, record_id, date, created_at, updated_at)
            VALUES (:id,:record_id, :date, :created_at, :updated_at)
            ON CONFLICT (record_id, date) DO NOTHING
            """
            batch_data = []
            created_at = updated_at = datetime.now(timezone.utc)
            for date in request.off_dates:
                batch_data.append({
                    "id": uuid4(),
                    "record_id": request.record_id,
                    "date": date,
                    "created_at": created_at,
                    "updated_at": updated_at})
                
            self.db.execute(text(query), batch_data)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to persist off days: {e}",
            )
        
    def get_availability_by_filter(self, filters: AvailabilityFilter):
        try:
            stmt = select(Availability)
            conditions = []

            # Dynamic record_id filter
            if filters.record_id:
                conditions.append(getattr(Availability, "record_id") == filters.record_id)
            # Common filters
            if filters.selected_date:
                conditions.append(getattr(Availability, "date") == filters.selected_date)
            if filters.start_time:
                conditions.append(getattr(Availability, "start_time") >= filters.start_time)
            if filters.end_time:
                conditions.append(getattr(Availability, "end_time") <= filters.end_time)
            if filters.availability_status:
                conditions.append(getattr(Availability, "availability_status") == filters.availability_status)
            if filters.availability_type:
                    conditions.append(getattr(Availability, "availabiliity_type") == filters.availability_type.value)
            if conditions:
                stmt = stmt.where(and_(*conditions))

            results = self.db.execute(stmt).scalars().all()
            return results
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch availability: {e}",
            )
        except Exception as e:
            logger.error(f"Unexpected error while fetching availability: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while fetching availability: {e}",
            )
    def update_availability_status(self, request, availability_status):
        try:
            query = f"""
            UPDATE availability
            SET availability_status = :availability_status
            WHERE record_id = :record_id
            AND date IN :dates
            """
            self.db.execute(text(query), {
                "availability_status": availability_status,
                "record_id": request.record_id,
                "dates": tuple(request.dates)
            })
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update availability status: {e}",
            )
        except Exception as e:
            logger.error(f"Unexpected error while updating availability status: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating availability status: {e}",
            )
    
    def get_availability(self, record_id, column_name, vals):
        try:
            query = f"""SELECT * FROM availability WHERE record_id=:record_id AND {column_name} IN :value"""
            availability = self.db.execute( text(query), {"record_id": record_id, "value": tuple(vals)}).fetchall()
            logger.info(f"Availability: {availability}")

            return [dict(row._mapping) for row in availability] if availability else []
        except Exception as e:
            logger.error(f"Error fetching item: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error while fetching availability for {record_id}.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
    def update_availability_status(self, availability_ids, status_value: str):
        try:
            # Normalize to list
            if not isinstance(availability_ids, Iterable) or isinstance(availability_ids, (str, bytes)):
                availability_ids = [availability_ids]

            query = text("""
                UPDATE availability
                SET availability_status = :availability_status
                WHERE id IN :availability_ids
            """).bindparams(bindparam("availability_ids", expanding=True))

            self.db.execute(query, {
                "availability_status": status_value,
                "availability_ids": availability_ids
            })

            self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update availability status: {e}",
            )
        
    def update_booking_status(self, booking_ids, status_value: str):
        try:
            # Normalize to list
            if not isinstance(booking_ids, Iterable) or isinstance(booking_ids, (str, bytes)):
                booking_ids = [booking_ids]
            query = text("""
                UPDATE booking
                SET status = :status
                WHERE id IN :booking_ids
            """).bindparams(bindparam("booking_ids", expanding=True))

            self.db.execute(query, {
                "status": status_value,
                "booking_ids": booking_ids
            })

            self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update booking status: {e}",
            )