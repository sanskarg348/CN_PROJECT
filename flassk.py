from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from main import get_data
from twilio.rest import Client
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    account_sid = 'AC738656904997b8323dbeb1dbcdc2cf45'
    auth_token = 'f41506e17ee276de585d18b95f637c6c'
    client = Client(account_sid, auth_token)
    msg = request.form.get('Body').split()
    keywords = " ".join(msg[:-1])
    limit = int(msg[-1])
    s1,s2,s3 = get_data(keywords, limit)
    message = client.messages.create(
        body=s1,
        from_='whatsapp:+14155238886',
        to=request.form.get('From')
    )
    message = client.messages.create(
        body=s2,
        from_='whatsapp:+14155238886',
        to=request.form.get('From')
    )
    message = client.messages.create(
        body=s3,
        from_='whatsapp:+14155238886',
        to=request.form.get('From')
    )
    resp = MessagingResponse()
    return str(resp)


if __name__ == "__main__":
    app.run(port=8000, debug=True)