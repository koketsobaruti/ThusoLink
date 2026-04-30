from ..schemas.business.bookings_schema import WhatsappBookingPayLoad

def booking_action_buttons(whatsapp_payload: WhatsappBookingPayLoad):

    return {
        "messaging_product": "whatsapp",
        "to": whatsapp_payload.to_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": whatsapp_payload.message_text},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"accept_{whatsapp_payload.booking_id}",
                            "title": "Accept"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"reject_{whatsapp_payload.booking_id}",
                            "title": "Reject"
                        }
                    }
                ]
            }
        }
    }