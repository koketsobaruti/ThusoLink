import httpx
from ..config.config import Settings
from ..utils.logger_utils import LoggerUtils

logger = LoggerUtils.get_logger("WhatsApp Client")

class WhatsAppClient:

    def __init__(self):
        self.settings = Settings()
        self.base_url = f"https://graph.facebook.com/{self.settings.VERSION}"
        self.headers = {
            "Authorization": f"Bearer {self.settings.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        self.phone_number_id = self.settings.WHATSAPP_PHONE_NUMBER_ID
        self.url = f"{self.base_url}/{self.phone_number_id}/messages"

    async def send(self, payload: dict):
        try:
            logger.info(f"Sending WhatsApp message via Phone ID: {self.phone_number_id} with WhatsApp API Version: {self.settings.VERSION}")
            async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(self.url, json=payload, headers=self.headers)

                    if response.status_code in (200, 201):
                        logger.info(f"WhatsApp message sent successfully for booking")
                        logger.info(f"Response: {response.text}")
                    else:
                        logger.error(f"Failed to send WhatsApp message: {response.status_code}")
                        logger.error(f"Response content: {response.text}")

                    response.raise_for_status()
                    return response.json()
        except httpx.RequestError as e:
            logger.error(f"Network error sending WhatsApp message: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp message: {str(e)}")
            