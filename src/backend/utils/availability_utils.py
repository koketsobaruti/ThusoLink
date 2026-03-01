from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from time import timezone
from uuid import uuid4
import uuid

from fastapi import HTTPException, status
from pydantic import ValidationError
from ..utils.logger_utils import LoggerUtils
from ..schemas.business.schedule_schema import AvailabilityRequest, AvailabilityType, SetOffDay
from ..schemas.business.bookings_schema import BookingType

logger = LoggerUtils.get_logger("Schedule Manager")

def check_availability_input(request: AvailabilityRequest):
    try:
        failed = []
        slots = request.slots 
        id = request.record_id
        # Validate slots in parallel
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(validate_and_insert_slot, idx, slot): idx for idx, slot in enumerate(slots)}
            for future in as_completed(futures):
                results.append(future.result())
        
        # Batch insert validated slots
        valid_slots = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "failed"]
        logger.info(f"Valid data: {valid_slots}")
        if valid_slots:
            try:
                timestamp = datetime.now(timezone.utc)
                batch_data = [{
                    "id": uuid4(),
                    "record_id": id,
                    "date": r["slot"].date,
                    "start_time": r["slot"].start_time,
                    "end_time": getattr(r["slot"], "end_time", r["slot"].start_time),
                    # set availability status to AVAILABLE by default, can be updated later based on bookings
                    "availability_status": r["slot"].availability_status.name if r["slot"].availability_status else "AVAILABLE",
                    "availabiliity_type": BookingType(request.request_type.value).name,
                    "created_at": timestamp,
                    "updated_at": timestamp,
                } for r in valid_slots]
                results = {"batch_data":batch_data,
                            "failed": failed,
                            "valid_slots":valid_slots}
                return results
            except HTTPException as e: 
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Failed to persist availability slots {e}.")
    except Exception as e: 
        logger.error(f"Unexpected error during availability validation: {e}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred during availability validation: {e}")

def validate_and_insert_slot(idx, slot):
    try:
        if slot.end_time is None:
            slot.end_time = slot.start_time
        elif slot.start_time > slot.end_time:
            logger.warning(f"Invalid slot time: start_time {slot.start_time} is after end_time {slot.end_time}")
            raise ValueError("Invalid slot time: start_time must be before end_time.")
        return {"index": idx,
                "slot": slot,
                "status": "success"}
    except (KeyError, ValueError) as e:
        return {"index": idx,
            "slot": slot,
            "status": "failed",
            "reason": str(e)}

from datetime import date

def validate_request(request: SetOffDay, user_id) -> None:
    if not user_id:
        raise ValueError("User ID is required")

    if not request.off_dates:
        raise ValueError("At least one off date must be provided")

    if any(d < date.today() for d in request.off_dates):
        raise ValueError("Off dates cannot be in the past")

    if len(set(request.off_dates)) != len(request.off_dates):
        raise ValueError("Duplicate off dates are not allowed")
    
    if request.request_type not in [type.value for type in AvailabilityType]:
        raise ValidationError("Invalid request type submitted")
    
    if not uuid.uuid4(str(request.record_id)):
        raise ValidationError("Invalid request input")
    
    if not all(map(lambda x: is_date_format(x), request.off_dates)):
        raise ValueError("Invalid date formats input")
    
@staticmethod
def is_date_format(value, date_format='%Y-%m-%d'):
    if not datetime.strptime(value, date_format):
        return True
    else:
        return False