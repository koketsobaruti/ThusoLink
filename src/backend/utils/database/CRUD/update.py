from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from ....utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Update Utils")
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
class UpdateUtils:
    def __init__(self, db: Session):
        self.db = db

    def generic_update(
        self,
        table_name: str,
        record_id,
        update_data: dict,
        id_column: str = "id"):

        if not update_data:
            raise ValueError("update_data cannot be empty")

        try:
            # Build SET clause safely
            set_clause = ", ".join([f"{col} = :{col}" for col in update_data.keys()])

            query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE {id_column} = :record_id
            """

            params = update_data.copy()
            params["record_id"] = record_id

            self.db.execute(text(query), params)
            self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database update failed: {e}",
            )
        except Exception as e:
            logger.error(f"Unexpected error during generic update: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected update error: {e}",
            )