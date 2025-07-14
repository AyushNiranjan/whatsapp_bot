from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from core_logic import get_next_message  # Import your logic here

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])  # ✅ Changed from /whatsapp to /webhook
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    user_id = request.values.get("From", "").split(":")[-1]  # Extract just the phone number

    # Process reply from core logic
    reply, done = get_next_message(user_id, incoming_msg)

    # Create Twilio-compatible response
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
