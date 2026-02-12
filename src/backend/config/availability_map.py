from ..models.business.schedule_model import (
    ServiceAvailability,
    BusinessAvailability,
    # StaffAvailability,
)
from ..utils.database.service_db_utils import ServiceDBUtils
from ..utils.database.db_utils import DBUtils
AVAILABILITY_MAP = {
    "service": (ServiceAvailability, "service_id"),
    "business": (BusinessAvailability, "business_id"),
    # "staff": (StaffAvailability, "staff_id"),
}

# mapping to verify ownership of the record for setting availability based on input
AVAILABILITY_CHECK_MAP={
    "service": ServiceDBUtils.verify_service_ownership,
    "business": DBUtils.user_business_exists,
}
