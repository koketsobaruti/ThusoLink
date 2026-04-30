from ..models.business.schedule_model import (
    ServiceAvailability,
    BusinessAvailability,
    # StaffAvailability,
)
from ..models.business.booking_model import (
    ServiceBooking,
    BusinessBooking
    # StaffAvailability,
)
# BOOKING_REGISTRY = {
#     "service": (ServiceBooking, ServiceAvailability),
#     "business": (BusinessBooking, BusinessAvailability)
#     }
BOOKING_REGISTRY = {
    "business": {
        "booking_model": BusinessBooking,
        "availability_model": BusinessAvailability,
        "provider_field": "business_id",
    },
    "service": {
        "booking_model": ServiceBooking,
        "availability_model": ServiceAvailability,
        "provider_field": "service_id",
    },
}