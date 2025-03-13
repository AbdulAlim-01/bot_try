from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Replace these with your actual credentials
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/641349695719475/messages"
ACCESS_TOKEN = "EAAeIBK9Ah2EBO8Df3xieVPED1JZCeEIZAcux0ME3MiRxLz7ZCrX1yZAbUtpZBiJzdZAT8oic4TrZCsZCcFAaHhTN5J7nS9DCNdPwP7Olj6NZCdeSSI2Vfbc6nqKuIdyXKVVLeKHAiHzJtDLV7uXVIi0fw6kIuJhXmyd2OiYNngT8dhQUHBAbWi8eJHbGWGk8LqvUxVZCJbvAcbtnIF3yvteIwZBpikHQslA3UkhIWIZD"

@app.route("/", methods=["GET"])
def verify():
    """Webhook verification (required by Meta)"""
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token = request.args.get("hub.verify_token")
    
    if mode == "subscribe" and token == "secret_token":
        return challenge
    return "Verification failed", 403

@app.route("/", methods=["POST"])
def webhook():
    """Handles incoming messages"""
    data = request.get_json()
    
    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                
                for msg in messages:
                    sender_id = msg["from"]
                    message_text = msg["text"]["body"]
                    
                    # Echo back the same message
                    send_whatsapp_message(sender_id, message_text)

    return "OK", 200

def send_whatsapp_message(to, text):
    """Send a message using WhatsApp Cloud API"""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
