from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from core_logic import get_next_message  # your dynamic logic

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    user_id = request.values.get("From", "").split(":")[-1]  # user phone number

    reply, done = get_next_message(user_id, incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
