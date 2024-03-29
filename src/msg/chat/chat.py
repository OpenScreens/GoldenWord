import json
import os
from urllib.parse import parse_qs
from flask import Flask, jsonify, render_template, request
import flask
import requests
import urllib


app = Flask(__name__)

# Define a function to add CORS headers to responses
def add_cors_headers(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'POST'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
	return response
    
# Apply the CORS headers to all routes using a Flask decorator
@app.after_request
def after_request(response):
	return add_cors_headers(response)

responses_array = []

@app.route('/')
def index():
	with open("../client/chat/chat.html") as f:
		html = f.read()
	return html

@app.route('/chat.js')
def chatjs():
	with open("../client/chat/chat.js","rb") as f:
		js = f.read()
	return js

@app.route('/chat.css')
def chatcss():
	with open("../client/chat/chat.css","rb") as f:
		css = f.read()
	return css

@app.route('/msg', methods=['GET'])
def msg():
	global responses_array
	emptyarray = responses_array
	responses_array = []
	return emptyarray
	
@app.route('/vuelta', methods=['POST'])
def post_vuelta():
	global responses_array
	post_vuelta = request.data.decode('utf-8')
	decoded_data = parse_qs(post_vuelta)
	response = decoded_data.get('response', [''])[0]
	chatid = decoded_data.get('chatid', [''])[0]
	print("response: " + response)
	data = {'response': response, 'chatid': chatid}
	responses_array.append(data)
	return jsonify(responses_array)

'''
@app.route('/array', methods=['POST'])
def post_array():
	post_array = request.data.decode('utf-8')
	decoded_data = parse_qs(post_array)
	message = decoded_data.get('message', [''])[0]

	data = {
		"message": message,
		"chatid": "123132",
		"frontend": "chatpage"
	}
	query_string = urllib.parse.urlencode(data)
	url = "https://pingpong.test.goldenwordai.com:4998"
	response = requests.post(url, data=query_string)
	return jsonify(data)
'''
@app.route('/array', methods=['POST'])
def post_array():
	json_data = flask.request.json
	url = "https://pingpong.test.goldenwordai.com:4998"
	requests.post(url, json=json_data)
	return json_data

if __name__ == '__main__':
	app.run(debug=True, threaded=True, port=5000)
