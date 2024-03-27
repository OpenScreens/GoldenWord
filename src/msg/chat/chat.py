import json
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Define a function to add CORS headers to responses
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response

# Apply the CORS headers to all routes using a Flask decorator
@app.after_request
def after_request(response):
    return add_cors_headers(response)

responses_array = []

@app.route('/msg', methods=['GET'])
def msg():
	global responses_array
	emptyarray = responses_array
	responses_array = []
	return emptyarray

@app.route('/array', methods=['GET'])
def post_array():
    url = "https://pingpong.test.goldenwordai.com:4998"

    data = {
        "message": "ping",
        "chatid": "1234",
        "frontend": "chatpage"
    }
    response = requests.post(url, json=data)

    # Agrega la respuesta al array
    responses_array.append(response.text)

    return response.text

if __name__ == '__main__':
	app.run(debug=True, threaded=True, port=5000)
