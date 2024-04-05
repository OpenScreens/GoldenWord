from urllib.parse import parse_qs
from flask import Flask, Response, jsonify, request
import flask
import requests

app = Flask(__name__)

def add_cors_headers(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
	return response

@app.after_request
def after_request(response):
	return add_cors_headers(response)

responses_array = []

@app.route('/')
def index():
	with open("client/chat/chat.html") as f:
		html = f.read()
	return html

@app.route('/chat.js')
def chatjs():
	with open("client/chat/chat.js","rb") as f:
		js = f.read()
	return js

@app.route('/chat.css')
def chatcss():
	with open("client/chat/chat.css","rb") as f:
		css = f.read()
	return Response(css, content_type='text/css')

@app.route('/msg', methods=['GET'])
def msg():
	global responses_array
	emptyarray = responses_array
	responses_array = []
	return emptyarray
	
@app.route('/vuelta', methods=['POST'])
def post_vuelta():
	global responses_array
	response = request.form.get('response')
	chatid = request.form.get('chatid')
	print("response: " + response)
	data = {'response': response, 'chatid': chatid}
	responses_array.append(data)
	return jsonify(responses_array)

@app.route('/array', methods=['POST'])
def post_array():
	json_data = flask.request.json
	url = "https://pingpong.test.goldenwordai.com:4998"
	requests.post(url, json=json_data)
	return json_data

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
