from flask import Flask, request
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from core_logic import get_next_message
import logging
import os

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def index():
    return "✅ WhatsApp Flask Bot is Running!"

@app.route("/webhook", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    user_id = request.values.get("From", "").split(":")[-1]

    if not incoming_msg or not user_id:
        logging.warning("⚠️ Invalid request: missing message or user ID")
        return "Invalid request", 400

    try:
        logging.info(f"📩 Incoming from {user_id}: {incoming_msg}")
        reply, done = get_next_message(user_id, incoming_msg)
    except Exception as e:
        logging.exception("❌ Error in core logic:")
        reply = "⚠️ Sorry, something went wrong. Please try again later."
        done = False

    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
