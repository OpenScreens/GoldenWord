import flask
from flask import request, jsonify
from flask import json
import requests
from dotenv import load_dotenv
import os
import logging
from openai import OpenAI
import pandas as pd
from buying_price import get_price
from twilio.twiml.messaging_response import MessagingResponse

app = flask.Flask(__name__)
app.debug = True
load_dotenv()

APP_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(APP_DIR+'/concesionaria.log')
logger.addHandler(file_handler)

openai_token = os.getenv('OPENAI_TOKEN')
openai_model = "gpt-4"
error_prefix = ""
conversations = {}

PROMPT_CLASSIFY_MODEL = 'gpt-4'
PROMPT_GENERIC_MODEL = 'gpt-4'
PROMPT_COLLECTVARS_MODEL = 'gpt-4'

client = OpenAI(api_key=openai_token)
session = requests.Session()

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

def call_chatgpt(prompt, messages, response_format=None, tokens=None, functions=None, function_call=None, model=None):
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
        logit_bias={96974: -100}
    )
    
    logger.debug(f"Call Chat GPT Response Details: {completion.choices[0].message.content}")
    return completion.choices[0].message

def load_prompt(filename):
    with open(os.path.join(APP_DIR, filename), 'r') as file:
        return file.read()

@app.route("/reload", methods=["GET"])
def reload_prompts():
    global prompt_classify
    prompt_classify = load_prompt('prompt_classify.txt')
    return jsonify({"status": "Prompts reloaded successfully"}), 200

def classify_prompt(user_input):
    prompt_classify = load_prompt('prompt_classify.txt')
    response = call_chatgpt(prompt_classify, [user_input], model=PROMPT_CLASSIFY_MODEL)
    return response.content.strip().lower()

def answer_generic(user_input):
    prompt_generic = load_prompt("prompt_generic.txt")
    response = call_chatgpt(prompt_generic,[user_input], model=PROMPT_GENERIC_MODEL)
    return response.content.strip().lower()

def collect_vars(user_input):
    prompt_collectvars = load_prompt("prompt_collectvars.txt")
    response = call_chatgpt(prompt_collectvars, [user_input], model=PROMPT_COLLECTVARS_MODEL)
    return response.content.strip().lower()

@app.route('/', methods=["POST"])
def receive_msg():
    data = request.json
    user_input = data.get('user_input')
    user_id = data.get('user_id')

    if not user_input or not user_id:
        response = jsonify({"error": "No user input or user ID provided"})
        return response, 400

    if user_id not in conversations:
        conversations[user_id] = {"state": "initial"}

    user_state = conversations[user_id]

    if user_state["state"] == "initial":
        prompt_type = classify_prompt(user_input)

        if prompt_type == "buying_price": ##perspectiva del usuario, el compra un auto es x aca
            user_state["state"] = "asking_details"
            return jsonify({"response": "Please provide the brand, model, and year of the car you are interested in (example: 'Toyota Corolla 2020')"}), 200
        
        elif prompt_type == "selling_price":
            json_response = collect_vars(user_input)
            print(json_response)
            car_details = json.loads(json_response)

            brand = car_details["brand"]
            model = car_details["model"]
            year = car_details["year"]
            mileage_magnitude = car_details["mileage_magnitude"]
            mileage_unit = car_details["mileage_unit"]
            print(brand, model, year, mileage_magnitude)
            
            missing_info = []
            for field, value in [("brand", brand), ("model", model), ("year", year), ("mileage", mileage_magnitude)]:
                if value == "":
                    missing_info.append(field)
            
            if missing_info:
                missing_info_str = ", ".join(missing_info)
                return jsonify({"response": f"Please provide the {missing_info_str}"}), 200
            
            brand, model, price, year, status = get_price(car_details["brand"].upper(), car_details["model"].upper(), int(car_details["year"]))
            
            depreciation_factor = 1 - (0.05 * float(mileage_magnitude) / 100000)
            calculated_price = price * max(depreciation_factor, 0.1)
            
            if status == 'exact':
                response = f"Based on the details provided for your {brand} {model} ({car_details['year']}) with {mileage_magnitude} {mileage_unit}, we can provide an estimated selling price of {calculated_price}."
            elif status == 'approximate':
                response = f"We don't have the exact price for your {brand} {model} from {car_details['year']}, but we have a ({year}) and considering {mileage_magnitude} {mileage_unit}, we estimated a selling price of {calculated_price}."
            elif status == 'no_price':
                response = f"We don't have price available for your {brand} {model} ({car_details['year']}) with {mileage_magnitude} {mileage_unit}."
            return jsonify({"response": response}), 200
        
        elif prompt_type == "loans":
            return jsonify({"response": "We don't accept loans"}), 200
        elif prompt_type == "generic":
            response = answer_generic(user_input)
            return jsonify({"response":response})
        elif prompt_type == "selling_process":
            return jsonify({"response":"When selling a car, you need a few documents." +
                             "First, the vehicle title or ownership document is essential as it proves you own the car."+
                               "You'll also need a bill of sale, which outlines the sale terms, including price and date."})
        elif prompt_type in ["selling_price", "buying_process"]:
            return jsonify({"response": f"We are working on {prompt_type}"}), 200
        else:
            return jsonify({"response": "We don't understand your prompt"}), 200

    elif user_state["state"] == "asking_selling_details":
        brand, model, year = user_input.split()
        user_state["state"] = "next_step_sell"
        user_state["car_details"] = {"brand": brand, "model": model, "year": year}
        return jsonify({"response": "Thank you for providing the details of your car. To give you an accurate selling price, we also need to know the mileage of your vehicle. How many kilometers has your car been driven? Please provide a number without 'km' or any punctuation. For example: 200000"})

    elif user_state["state"] == "asking_details":
        try:
            brand, model, year = user_input.split()
            brand, model, price, year, status = get_price(brand.upper(), model.upper(), int(year))
            user_state["state"] = "initial"
            return jsonify({"response": f"The price for a {brand} {model} from {year} is: {price}"}), 200
        except ValueError:
            return jsonify({"response": "Invalid input. Please provide the brand, model, and year separated by spaces."}), 400

    response = jsonify({"response": "An unexpected error occurred"})
    return response, 500

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    data = {
        "user_input": incoming_msg,
        "user_id": 123
    }
    response = requests.post('http://localhost:5000/', json=data)
    response_data = response.json()
    msg.body(response_data.get('response', 'An error occurred'))

    return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
