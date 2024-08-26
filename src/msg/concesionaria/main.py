import flask
from flask import request, jsonify
import requests
from dotenv import load_dotenv
import os
import logging
from openai import OpenAI
import pandas as pd
from buying_price import get_price

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

        if prompt_type == "buying_price":
            user_state["state"] = "asking_details"
            return jsonify({"response": "Please provide the brand, model, and year of the car you are interested in (example: 'Toyota Corolla 2020')"}), 200
        elif prompt_type == "loans":
            return jsonify({"response": "We don't accept loans"}), 200
        elif prompt_type in ["selling_price", "selling_process", "buying_process"]:
            return jsonify({"response": f"We are working on {prompt_type}"}), 200
        else:
            return jsonify({"response": "We don't understand your prompt"}), 200

    elif user_state["state"] == "asking_details":
        try:
            brand, model, year = user_input.split()
            brand, model, price = get_price(brand.upper(), model.upper(), int(year))
            user_state["state"] = "initial"
            return jsonify({"response": f"The price for a {brand} {model} from {year} is: {price}"}), 200
        except ValueError:
            return jsonify({"response": "Invalid input. Please provide the brand, model, and year separated by spaces."}), 400

    response = jsonify({"response": "An unexpected error occurred"})
    return response, 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
