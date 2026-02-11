import httpx
from ...config.config import Settings
import json
import aiohttp
from ...modules.business.booking_manager import WhatsAppBookingDetails
from ...utils.logger_utils import LoggerUtils
from ...services import client, messages
from ...schemas.business.bookings_schema import WhatsappBookingPayLoad, BookingRequest, BookingStatus, BookingUpdate, WhatsAppBookingDetails
logger = LoggerUtils.get_logger("Whatsapp Service")

class WhatsAppService:
    def __init__(self):
        self.settings = Settings()
        # self.base_url = f"https://graph.facebook.com/{self.settings.VERSION}"

    async def send_booking_request(self, booking, message_text):

        # phone_number_id = self.settings.WHATSAPP_PHONE_NUMBER_ID
        # # url = f"{self.base_url}/{phone_number_id}/messages"

        # logger.info(f"Sending WhatsApp message via Phone ID: {phone_number_id}")
        # logger.info(f"WhatsApp API Version: {self.settings.VERSION}")

        # headers = {
        #     "Authorization": f"Bearer {self.settings.ACCESS_TOKEN}",
        #     "Content-Type": "application/json"
        # }

        whatsapp_payload = WhatsappBookingPayLoad(
            message_text=message_text,      
            booking_id=booking.id,
            to_number=self.settings.RECIPIENT_WAID
        )
        data = messages.booking_action_buttons(whatsapp_payload)
        response = await client.WhatsAppClient().send(payload=data)
        if response:
            logger.info(f"WhatsApp message sent successfully for booking {booking.id}")
            logger.info(f"Response: {response}")
        # try:
        #     response = await client.WhatsAppClient().send(payload = data)
        #     # async with httpx.AsyncClient(timeout=30.0) as client:
        #     #     response = await client.post(url, json=data, headers=headers)

        #     # if response.status_code in (200, 201):
        #     #     logger.info(f"WhatsApp message sent successfully for booking {booking.id}")
        #     #     logger.info(f"Response: {response.text}")
        #     # else:
        #     #     logger.error(f"Failed to send WhatsApp message: {response.status_code}")
        #     #     logger.error(f"Response content: {response.text}")

        # except httpx.RequestError as e:
        #     logger.error(f"Network error sending WhatsApp message: {str(e)}")

        # except Exception as e:
        #     logger.error(f"Unexpected error sending WhatsApp message: {str(e)}")
            
# class WhatsAppService:
#     def __init__(self):
#         self.settings = Settings()
#     async def send_booking_request(self, booking, message_text):
#         phone_number_id = self.settings.WHATSAPP_PHONE_NUMBER_ID
#         logger.info(f"Sending WhatsApp message to phone number ID: {phone_number_id}")
#         logger.info(f"WhatsApp token (first 20 chars): {self.settings.WHATSAPP_TOKEN[:20]}")
#         logger.info(f"WhatsApp API version: {self.settings.VERSION}")
#         headers = {
#             "Authorization": f"Bearer {self.settings.WHATSAPP_TOKEN}",
#             "Content-Type": "application/json"}
#         data = {
#                 "messaging_product": "whatsapp",
#                 "to": self.settings.RECIPIENT_WAID,
#                 "type": "interactive",
#                 "interactive": {
#                     "type": "button",
#                     "body": {"text": message_text},
#                     "action": {
#                         "buttons": [
#                             {"type": "reply", "reply": {"id": f"accept_{booking.id}", "title": "Accept"}},
#                             {"type": "reply", "reply": {"id": f"reject_{booking.id}", "title": "Reject"}}
#                         ]
#                     }
#                 }
#             }
#         async with aiohttp.ClientSession() as session:
#             url = f"https://graph.facebook.com/{self.settings.VERSION}/{self.settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
#             try:
#                 async with session.post(url, json = data, headers=headers) as response:
#                     text = await response.text()
#                     if response.status in (200, 201):
#                         logger.info(f"WhatsApp message sent successfully for booking {booking.id}")
#                         logger.info(f"Response: {text}")
#                     else:
#                         logger.error(f"Failed to send WhatsApp message: {response.status}")
#                         logger.error(f"Response content: {text}")
#             except aiohttp.ClientError as e:
#                 logger.error(f"Error sending WhatsApp message: {e}")


        #     response = await client.post(url, json=data, headers=headers)
        #     response.raise_for_status()
        # url = f"https://graph.facebook.com/v17.0/{Settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

        # headers = {
        #     "Authorization": f"Bearer {Settings.WHATSAPP_TOKEN}",
        #     "Content-Type": "application/json"
        # }

        # data = {
        #     "messaging_product": "whatsapp",
        #     "to": details.provider_whatsapp_number,
        #     "type": "interactive",
        #     "interactive": {
        #         "type": "button",
        #         "body": {"text": message_text},
        #         "action": {
        #             "buttons": [
        #                 {"type": "reply", "reply": {"id": f"accept_{booking.id}", "title": "Accept"}},
        #                 {"type": "reply", "reply": {"id": f"reject_{booking.id}", "title": "Reject"}}
        #             ]
        #         }
        #     }
        # }

        # async with httpx.AsyncClient() as client:
        #     response = await client.post(url, json=data, headers=headers)
        #     response.raise_for_status()