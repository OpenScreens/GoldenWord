import logging
import flask
from flask import request, jsonify
import requests
import os
from openai import OpenAI
import pandas as pd
from buying_price import get_price
import tiktoken
import requests
from env import OPENAI_TOKEN
from prompt_classify import output_prompt, BRANCHES
import threading

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

# Function to get logit bias
def get_logit_bias(branches):
    logit_bias = {}
    encoding = tiktoken.encoding_for_model("gpt-4")
    for i, qt in enumerate(branches):
        tokens = encoding.encode(qt['key'])
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
    response = call_chatgpt(output_prompt(), [user_input], model=PROMPT_CLASSIFY_MODEL, logit_bias=True)
    return response.content.strip().lower()

# Function to answer generic prompt
def answer_generic(user_input):
    return "I'm not trained to handle that question. Please contact +5491158918239"


@app.route('/reload')
def prompts():
    global prompt_make, prompt_model, prompt_yearcar, prompt_milleagevalue, prompt_milleageunit
    prompt_make = load_prompt("prompt_make2.txt")
    prompt_model = load_prompt("prompt_model.txt")
    prompt_yearcar = load_prompt("prompt_yearcar.txt")
    prompt_milleagevalue = load_prompt("prompt_milleagevalue.txt")
    prompt_milleageunit = load_prompt("prompt_milleageunit.txt")

prompts()

# Function to collect variables
def collect_vars(user_input):
    # Cargar los prompts

    results = [None] * 5

    def call_gpt(index, prompt):
        results[index] = (call_chatgpt(prompt, [user_input], model=PROMPT_COLLECTVARS_MODEL, logit_bias=False)).content.strip().lower()

    threads = [
        threading.Thread(target=call_gpt, args=(0, prompt_make)),
        threading.Thread(target=call_gpt, args=(1, prompt_model)),
        threading.Thread(target=call_gpt, args=(2, prompt_yearcar)),
        threading.Thread(target=call_gpt, args=(3, prompt_milleagevalue)),
        threading.Thread(target=call_gpt, args=(4, prompt_milleageunit)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    r1, r2, r3, r4, r5 = results
    return r1, r2, r3, r4, r5

def send_response(user_id, response_message, url):
    response_data = {
        "user_id": user_id,
        "response": response_message
    }
    requests.post(url, json=response_data)

# Receive message route
@app.route('/', methods=["POST"])
def receive_msg():
    # Extract user input and user ID from the incoming json
    data = request.json
    user_input = data.get('user_input')
    user_id = data.get('user_id')
    frontend_url = data.get('frontend_url')
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
            make,model,yearp,milleagevalue,millageunit = collect_vars(" ".join(user_state['conversation']))
            print(make,model,yearp,milleagevalue,millageunit)
            
            # Check for missing information
            missing_info = []
            for field, value in [("make", make), ("model", model), ("year", yearp), ("mileage", milleagevalue), ("mileage unit", millageunit)]:
                if value == '""':
                    missing_info.append(field)
            
            if missing_info:
                missing_info_str = ", ".join(missing_info)
                user_state['state'] = "asking_missing_info"
                send_response(user_id,f"Please provide the {missing_info_str}",frontend_url)
                return ('ok'), 200
            
            # Calculate and return the selling price
            brand, model, price, year, status = get_price(make.upper(), model.upper(), int(yearp))
            
            # Despreciation formula value according to the miles
            depreciation_factor = 1 - (0.05 * float(milleagevalue) / 100000)
            calculated_price = price * max(depreciation_factor, 0.1) * 3
            
            # If there is price for the exact year entered or approximate or there is not price (See get_price)
            if status == 'exact':
                response = f"Based on the details provided for your {brand} {model} ({yearp}) with {milleagevalue} {millageunit}, we can provide an estimated selling price of {calculated_price}."
            elif status == 'approximate':
                response = f"We don't have the exact price for your {brand} {model} from {yearp}, but we have a ({year}) and considering {milleagevalue} {millageunit}, we estimated a selling price of {calculated_price}."
            elif status == 'no_price':
                response = f"We don't have price available for your {brand} {model} ({yearp}) with {milleagevalue} {millageunit}."
            user_state['state'] = 'initial'
            
            user_state['conversation'] = []
            send_response(user_id,response,frontend_url)
            return ('ok'), 200

        # Other prompts types
        elif prompt_type == "loans":
            user_state['state'] = 'initial'
            response = "We don't accept loans"
        elif prompt_type == "generic":
            user_state['state'] = 'initial'
            response = answer_generic(user_input)
        elif prompt_type == "selling_process":
            user_state['state'] = 'initial'
            response = ("When selling a car, you need a few documents. "
                        "First, the vehicle title or ownership document is essential as it proves you own the car. "
                        "You'll also need a bill of sale, which outlines the sale terms, including price and date.")
        elif prompt_type in ["selling_price", "buying_process"]:
            user_state['state'] = 'initial'
            response = f"We are working on {prompt_type}"
        else:
            user_state['state'] = 'initial'
            response = "We don't understand your prompt"
        
        user_state['conversation'] = []
        send_response(user_id,response,frontend_url)


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
