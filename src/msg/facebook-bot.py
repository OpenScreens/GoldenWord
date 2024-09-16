import os
from flask import Flask, request
import logging
import requests
from env import WHATSAPP_VERIFY_TOKEN, FB_AUTH_TOKEN, SERVERURL

app = Flask(__name__)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(APP_DIR+'/facebook.log')
logger.addHandler(file_handler)

# Verify token facebook
@app.route('/facebook', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == WHATSAPP_VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return 'Verificación fallida', 403

#Facebook Route
@app.route('/facebook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    if 'entry' in data:
        for entry in data['entry']:
            if 'messaging' in entry:
                for event in entry['messaging']:
                    if 'message' in event:
                        sender_id = event['sender']['id']
                        message_text = event['message']['text']
                        handle_message(sender_id, message_text)
    return "Evento recibido", 200

# Handle msg facebook
def handle_message(sender_id, msg_body):
    data = {
        "user_input": msg_body,
        "user_id": sender_id
    }
    response = requests.post(SERVERURL, json=data)
    response_data = response.json()
    response_final = (response_data.get('response', 'An error occurred'))
    snd_msg_facebook(sender_id, response_final)

# Send msg to facebook
def snd_msg_facebook(recipient_id, message_text):
    url = 'https://graph.facebook.com/v11.0/me/messages'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text},
        'access_token': FB_AUTH_TOKEN
    }
    response = requests.post(url, json=data, headers=headers)
    print(f'Status: {response.status_code}, Response: {response.json()}')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
