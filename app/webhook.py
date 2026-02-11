from fastapi import FastAPI, Request, Query
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
import requests

load_dotenv()

app = FastAPI()

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
    try:
        phone_number_id = os.environ.get("WHATSAPP_BUSINESS_PHONE_NUMBER_ID")
        access_token = os.environ.get("ACCESS_TOKEN")
        
        if not phone_number_id or not access_token:
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

        response = await requests.post(url, headers=headers, json=data)
        
        response_data = response.json()
        
        if response.status_code in [200, 201]:
            return response.status_code
        else:
            return {"error": "Failed to send message", "details": response_data}, response.status_code

    except Exception as e:
        return {"error": str(e)}, 500

###########################################################################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
