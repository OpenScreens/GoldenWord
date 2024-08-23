import time
from urllib.parse import urlencode
import flask
from flask import request, jsonify
import threading
import requests
from dotenv import load_dotenv
import os
import logging
import json
import yaml
json.loads = yaml.load
from openai import OpenAI

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

PROMPT_BRANCH_MODEL = 'gpt-4'

client = OpenAI(api_key=openai_token)
session = requests.Session()

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
    classification_prompt = prompt_classify + f"\nUser input: {user_input}"
    response = call_chatgpt(classification_prompt, [], model=PROMPT_BRANCH_MODEL)
    return response.content.strip().lower()

@app.route('/', methods=["POST"])
def receive_msg():
    data = request.json
    user_input = data.get('user_input')
    
    if not user_input:
        return jsonify({"error": "No user input provided"}), 400

    prompt_type = classify_prompt(user_input)
    
    if prompt_type == "unknown":
        return jsonify({"error": "Unable to classify the request"}), 400


    response = f"{prompt_type}"
    
    return jsonify({"response": response}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
