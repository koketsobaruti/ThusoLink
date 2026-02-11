from .client import WhatsAppClient
from .messages import booking_action_buttons

client = WhatsAppClient()


async def send_booking_request(details, booking, message_text):

    payload = booking_action_buttons(
        message_text=message_text,
        booking_id=str(booking.id),
        to_number=details["provider_whatsapp_number"]
    )

    return await client.send(payload)