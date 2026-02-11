import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
phone_number_id = os.environ.get("WHATSAPP_BUSINESS_PHONE_NUMBER_ID")
access_token = os.environ.get("ACCESS_TOKEN")
to_phone_number = "201147372828"  # Replace with recipient's phone number (include country code, no +)
template_name = "pro_wash_v3"  # Template name from Meta dashboard
language_code = "ar"  # Arabic language code

# API endpoint
url = f"https://graph.facebook.com/v16.0/{phone_number_id}/messages"

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Request body
data = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": to_phone_number,
    "type": "template",
    "template": {
        "name": template_name,
        "language": {
            "code": language_code
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
                            "flow_token": "unused",  # Optional, default is "unused"
                            # "flow_action_data": {}  # Optional, JSON object with data payload for the first screen
                        }
                    }
                ]
            }
        ]
    }
}

# Make the request
response = requests.post(url, headers=headers, json=data)

# Print response
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text}")
