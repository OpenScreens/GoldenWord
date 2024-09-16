import json
import os
from flask import Flask, request, jsonify
import logging
import requests
from env import WHATSAPP_VERIFY_TOKEN, WPP_AUTH_TOKEN, SERVERURL

app = Flask(__name__)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(APP_DIR+'/whatsapp.log')
logger.addHandler(file_handler)

urlwpp = "https://graph.facebook.com/v20.0/262736246918040/messages"

# WhatsApp route
@app.route("/whatsapp", methods=['GET'])
def whatsapp_verify():
    token_sent = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token_sent == WHATSAPP_VERIFY_TOKEN:
        return str(challenge)
    return 'Token de verificación no válido', 403

@app.route("/whatsapp", methods=['POST'])
def whatsapp_post():
    incoming_data = request.get_json()
    print(f"Data received: {incoming_data}")
    logger.info(f"Data Incoming: {incoming_data}")
    
    if incoming_data and 'entry' in incoming_data:
        entry = incoming_data['entry'][0]
        changes = entry.get('changes', [])
        if changes:
            value = changes[0].get('value', {})
            messages = value.get('messages', [])
            if messages:
                message = messages[0]
                msg_body = message['text']['body']
                sender_id = message['from']
                sender_name = value['contacts'][0]['profile']['name']
                print(f"Mensaje recibido de {sender_name} ({sender_id}): {msg_body}")
                
                if msg_body and sender_id:
                    data = {
                        "user_input": msg_body,
                        "user_id": sender_id
                    }
                    response = requests.post(SERVERURL, json=data)
                    response_data = response.json()
                    response_final = (response_data.get('response', 'An error occurred'))
                    try:
                        sender_id = sender_id.replace("9","",1)
                        send_msg_wpp(sender_id,response_final,message)

                    except Exception as e:
                        print(e)
                        return jsonify({"response": "An unexpected error occurred"}), 500
                
                return ('Ok'), 200
    return jsonify({"status": "error", "message": "No message found"}), 200
 
# Send Msg whatsapp function
def send_msg_wpp(number, msg, message):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {
            "body": msg
        },
        "context": {
          'message_id': message['id'],
        },
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {WPP_AUTH_TOKEN}'
        }

    response = requests.request("POST", urlwpp, headers=headers, data=payload)

    data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message['id'],
    }
    response = requests.post(urlwpp, headers=headers, json=data)

    print(response.text)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
