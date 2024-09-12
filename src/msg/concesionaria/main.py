import flask
from flask import request, jsonify
from flask import json
import requests
import os
import logging
from openai import OpenAI
import pandas as pd
from buying_price import get_price
import tiktoken
import requests
import json
from env import OPENAI_TOKEN, WHATSAPP_VERIFY_TOKEN, WPP_AUTH_TOKEN, FB_AUTH_TOKEN

app = flask.Flask(__name__)
app.debug = True

APP_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(APP_DIR+'/concesionaria.log')
logger.addHandler(file_handler)


openai_model = "gpt-4"
error_prefix = ""
conversations = {}

PROMPT_CLASSIFY_MODEL = 'gpt-4'
PROMPT_GENERIC_MODEL = 'gpt-4'
PROMPT_COLLECTVARS_MODEL = 'gpt-4'

client = OpenAI(api_key=OPENAI_TOKEN)
session = requests.Session()

BRANCHES = {
    "buying_price": [
        '"I want to buy a Nissan March 2015, how much would that be?"',
        '"What is the price of a 2018 Toyota Corolla?"',
        '"How much does a Honda Civic 2020 cost?"'
    ],
    "selling_price": [
        '"What is the selling price of my 2018 Honda Civic?"',
        '"I want to sell my honda civic 2008"'
    ],
    "selling_process": [
        '"What documents do I need to sell my car?"'
    ],
    "buying_process": [
        '"How do I buy a car?"'
    ],
    "selling_documents": [
        '"What paperwork is required to sell a vehicle?"'
    ],
    "loans": [
        '"Can I get a loan to buy a car?"'
    ],
    "generic": [
        '"Tell me about car insurance."'
    ]
}

# Function to get logit bias
def get_logit_bias(branches):
    logit_bias = {}
    encoding = tiktoken.encoding_for_model("gpt-4")
    for branch, sentences in branches.items():
            tokens = encoding.encode(branch)
            for token in tokens:
                logit_bias[token] = 10
   
    logger.debug(f"Logit bias: {logit_bias}")
    return logit_bias

# Function to add CORS headers
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

# Chat.html route
@app.route('/')
def index():
	with open("../chatpopup/chat.html") as f:
		html = f.read()
	return html

# Function to call ChatGPT
def call_chatgpt(prompt, messages, response_format=None, tokens=None, functions=None, function_call=None, model=None, logit_bias=True):
    if model is None:
        raise Exception("No model assigned for GPT")
    if response_format is None:
        response_format = "text"
    if model == "gpt-4":
        response_format = "text"
    
    conversation = [{"role": "system", "content": prompt}]
    for i, message in enumerate(messages):
        if i != 0:
            conversation.append({"role": "assistant", "content": "[..]"})
        conversation.append({"role": "user", "content": message})
    
    logger.debug(f"Call Chat GPT Request Details: content: {conversation}, response_format: {response_format}")
    
    completion = client.chat.completions.create(
        model=model,
        temperature=0,
        seed=1,
        response_format={"type": response_format},
        messages=conversation,
        functions=functions,
        function_call=function_call,
        logit_bias=get_logit_bias(BRANCHES) if logit_bias else None
    )
    
    logger.debug(f"Call Chat GPT Response Details: {completion.choices[0].message.content}")
    return completion.choices[0].message

# Function to load prompt from .txt file
def load_prompt(filename):
    with open(os.path.join(APP_DIR, filename), 'r') as file:
        return file.read()

# Function to classify prompt
def classify_prompt(user_input):
    prompt_classify = load_prompt('prompt_classify.txt')
    response = call_chatgpt(prompt_classify, [user_input], model=PROMPT_CLASSIFY_MODEL, logit_bias=True)
    return response.content.strip().lower()

# Function to answer generic prompt
def answer_generic(user_input):
    prompt_generic = load_prompt("prompt_generic.txt")
    response = call_chatgpt(prompt_generic,[user_input], model=PROMPT_GENERIC_MODEL, logit_bias=False)
    return response.content.strip().lower()

# Function to collect variables
def collect_vars(user_input):
    prompt_collectvars = load_prompt("prompt_collectvars.txt")
    response = call_chatgpt(prompt_collectvars, [user_input], model=PROMPT_COLLECTVARS_MODEL,logit_bias=False)
    return response.content.strip().lower()

# Receive message route
@app.route('/', methods=["POST"])
def receive_msg():
    # Extract user input and user ID from the incoming json
    data = request.json
    user_input = data.get('user_input')
    user_id = data.get('user_id')
    print (user_id)

    # Check if user input or user ID is missing
    if not user_input or not user_id:
        response = jsonify({"error": "No user input or user ID provided"})
        return response, 400

    # Initialize or update the conversation state for the user
    if user_id not in conversations:
        conversations[user_id] = {"state": "initial", "conversation": []}

    user_state = conversations[user_id]
    # Add the userinput to the conversation history
    user_state['conversation'].append(user_input) 

    # First Step
    if user_state["state"] == "initial":
        # Classify the userinput to determine the category
        prompt_type = classify_prompt(user_input)
        user_state['state'] = 'classify'
        user_state['branch'] = prompt_type
        logger.debug(user_state)
        print(user_state)

    if user_state['state'] == "classify" or user_state['state'] == 'asking_missing_info':
        prompt_type = user_state['branch']
        
        if prompt_type == "buying_price":
            user_state["state"] = "asking_details"
            return jsonify({"response": "Please provide the brand, model, and year of the car you are interested in (example: 'Toyota Corolla 2020')"}), 200
        
        elif prompt_type == "selling_price":
            # Collect variables from userinput needed for selling price calculation
            json_response = collect_vars(" ".join(user_state['conversation']))
            print(json_response)
            car_details = json.loads(json_response)

            brand = car_details["brand"]
            model = car_details["model"]
            year = car_details["year"]
            mileage_magnitude = car_details["mileage_magnitude"]
            mileage_unit = car_details["mileage_unit"]
            print(brand, model, year, mileage_magnitude)
            
            # Check for missing information
            missing_info = []
            for field, value in [("brand", brand), ("model", model), ("year", year), ("mileage", mileage_magnitude)]:
                if value == "":
                    missing_info.append(field)
            
            if missing_info:
                missing_info_str = ", ".join(missing_info)
                user_state['state'] = "asking_missing_info"
                return jsonify({"response": f"Please provide the {missing_info_str}"}), 200
            
            # Calculate and return the selling price
            brand, model, price, year, status = get_price(car_details["brand"].upper(), car_details["model"].upper(), int(car_details["year"]))
            
            # Despreciation formula value according to the miles
            depreciation_factor = 1 - (0.05 * float(mileage_magnitude) / 100000)
            calculated_price = price * max(depreciation_factor, 0.1) * 3
            
            # If there is price for the exact year entered or approximate or there is not price (See get_price)
            if status == 'exact':
                response = f"Based on the details provided for your {brand} {model} ({car_details['year']}) with {mileage_magnitude} {mileage_unit}, we can provide an estimated selling price of {calculated_price}."
            elif status == 'approximate':
                response = f"We don't have the exact price for your {brand} {model} from {car_details['year']}, but we have a ({year}) and considering {mileage_magnitude} {mileage_unit}, we estimated a selling price of {calculated_price}."
            elif status == 'no_price':
                response = f"We don't have price available for your {brand} {model} ({car_details['year']}) with {mileage_magnitude} {mileage_unit}."
            user_state['state'] = 'initial'
            return jsonify({"response": response}), 200
        
        # Other prompts types
        elif prompt_type == "loans":
            user_state['state'] = 'initial'
            return jsonify({"response": "We don't accept loans"}), 200
        elif prompt_type == "generic":
            user_state['state'] = 'initial'
            response = answer_generic(user_input)
            return jsonify({"response":response})
        elif prompt_type == "selling_process":
            user_state['state'] = 'initial'
            return jsonify({"response":"When selling a car, you need a few documents." +
                             "First, the vehicle title or ownership document is essential as it proves you own the car."+
                               "You'll also need a bill of sale, which outlines the sale terms, including price and date."})
        elif prompt_type in ["selling_price", "buying_process"]:
            user_state['state'] = 'initial'
            return jsonify({"response": f"We are working on {prompt_type}"}), 200
        else:
            user_state['state'] = 'initial'
            return jsonify({"response": "We don't understand your prompt"}), 200

    elif user_state["state"] == "asking_details":
        try:
            # Extract car details from user input
            brand, model, year = user_input.split()
            brand, model, price, year, status = get_price(brand.upper(), model.upper(), int(year))
            user_state["state"] = "initial"
            return jsonify({"response": f"The price for a {brand} {model} from {year} is: {price}"}), 200
        except ValueError:
            return jsonify({"response": "Invalid input. Please provide the brand, model, and year separated by spaces."}), 400
    response = jsonify({"response": "An unexpected error occurred"})
    return response, 200

# WhatsApp route
@app.route("/whatsapp", methods=['GET', 'POST'])
def whatsapp_reply():
    if request.method == 'GET':
        token_sent = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token_sent == WHATSAPP_VERIFY_TOKEN:
            return str(challenge)
        return 'Token de verificación no válido', 403
    elif request.method == 'POST':
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
                        response = requests.post('http://localhost:5000/', json=data)
                        response_data = response.json()
                        response_final = (response_data.get('response', 'An error occurred'))
                        try:
                            sender_id = sender_id.replace("9","",1)
                            send_msg_wpp(sender_id,response_final,message)

                            headers = {
                                'Authorization': f'Bearer {WPP_AUTH_TOKEN}',
                                'Content-Type': 'application/json'
                            }
                            data = {
                                "messaging_product": "whatsapp",
                                "status": "read",
                                "message_id": message['id'],
                            }
                            response = requests.post("https://graph.facebook.com/v20.0/262736246918040/messages", headers=headers, json=data)
                        except Exception as e:
                            print(e)
                            return jsonify({"response": "An unexpected error occurred"}), 500
                  
                    return ('Ok'), 200
        return jsonify({"status": "error", "message": "No message found"}), 200
 
# Send Msg whatsapp function
def send_msg_wpp(number, msg, message):
    url = "https://graph.facebook.com/v20.0/262736246918040/messages"
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

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

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
    response = requests.post('http://localhost:5000/', json=data)
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
    app.run(host='0.0.0.0', port=5000)
