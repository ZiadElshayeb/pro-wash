from fastapi import FastAPI, Request, Query
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
import httpx
import logging
from datetime import datetime

load_dotenv()

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SendMessageRequest(BaseModel):
    to: str
    template_name: str = "pro_wash_v3"
    language_code: str = "ar"
    consumption_id: str = "unused"

# POST - API to send WhatsApp messages
@app.post("/send-message")
async def send_whatsapp_message(payload: SendMessageRequest):
    """
    API Endpoint to send a template message to a WhatsApp user.
    """
    start_time = datetime.now()

    logger.info(f"Request received - To: {payload.to}, Template: {payload.template_name}, consumption id: {payload.consumption_id}")

    try:
        phone_number_id = os.environ.get("WHATSAPP_BUSINESS_PHONE_NUMBER_ID")
        access_token = os.environ.get("ACCESS_TOKEN")
        
        if not phone_number_id or not access_token:
            logger.error("Missing environment variables for WhatsApp API")
            return {"error": "Missing environment variables for WhatsApp API"}, 500

        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": payload.to,
            "type": "template",
            "template": {
                "name": payload.template_name,
                "language": {
                    "code": payload.language_code
                },
                "components": [
                    {
                        "type": "button",
                        "sub_type": "flow",
                        "index": "0",
                        "parameters": [
                            {
                                "type": "action",
                                "action": {
                                    "flow_token": payload.consumption_id
                                }
                            }
                        ]
                    }
                ]
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
        
        response_data = response.json()

        duration = (datetime.now() - start_time).total_seconds()
        
        if response.status_code in [200, 201]:
            logger.info(f"Success - Status: {response.status_code}, To: {payload.to}, Duration: {duration}s")
            return response.status_code
        else:
            logger.error(f"Failed - Status: {response.status_code}, To: {payload.to}, Error: {response_data}, Duration: {duration}s")
            return {"error": "Failed to send message", "details": response_data}, response.status_code

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.exception(f"Exception occurred - To: {payload.to}, Duration: {duration}s, Error: {str(e)}")
        return {"error": str(e)}, 500

###########################################################################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
