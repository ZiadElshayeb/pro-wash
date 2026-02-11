from fastapi import FastAPI, Request, Query
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.environ.get("ACCESS_TOKEN")  # Set your own verify token


# GET - Webhook verification (Meta will call this to verify your endpoint)
@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_token == VERIFY_TOKEN:
        print("Webhook verified!")
        return int(hub_challenge)
    else:
        return {"error": "Forbidden"}, 403


# POST - Receive messages and flow responses
@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print(f"Received webhook: {json.dumps(data, indent=2, ensure_ascii=False)}")

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])

                for message in messages:
                    sender = message.get("from")  # sender phone number
                    msg_type = message.get("type")

                    # Flow response comes as "interactive" type with "nfm_reply"
                    if msg_type == "interactive":
                        interactive = message.get("interactive", {})
                        interactive_type = interactive.get("type")

                        if interactive_type == "nfm_reply":
                            # This is the flow response!
                            response_json = interactive.get("nfm_reply", {}).get("response_json", "{}")
                            flow_response = json.loads(response_json)

                            print(f"===== FLOW RESPONSE =====")
                            print(f"From: {sender}")
                            print(f"Flow data: {json.dumps(flow_response, indent=2, ensure_ascii=False)}")
                            print(f"=========================")

                            # TODO: Process the flow response here
                            # e.g., save to database, send confirmation, etc.

    except Exception as e:
        print(f"Error processing webhook: {e}")

    # Always return 200 to acknowledge receipt
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
