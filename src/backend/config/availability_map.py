from ..models.business.schedule_model import (
    ServiceAvailability,
    BusinessAvailability,
    # StaffAvailability,
)

AVAILABILITY_MAP = {
    "service": (ServiceAvailability, "service_id"),
    "business": (BusinessAvailability, "business_id"),
    # "staff": (StaffAvailability, "staff_id"),
}
