from concurrent.futures import ThreadPoolExecutor, as_completed
from uuid import uuid4

from fastapi import HTTPException, status
from ..utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Schedule Manager")

def check_availability_input(id, slots):
        failed = []
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
                batch_data = [{
                    "schedule_id": uuid4(),
                    "id": id,
                    "date": r["slot"].date,
                    "start_time": r["slot"].start_time,
                    "end_time": getattr(r["slot"], "end_time", r["slot"].start_time),
                    "availability_status": r["slot"].availability_status.name
                } for r in valid_slots]
                results = {"batch_data":batch_data,
                            "failed": failed,
                            "valid_slots":valid_slots}
                return results
            except HTTPException as e: 
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Failed to persist availability slots {e}.")

def validate_and_insert_slot(idx, slot):
    try:
        if slot.start_time > slot.end_time:
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
    