import json
from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('chat.html')


@app.route('/msg', methods=['GET'])
def msg():
	url = "http://127.0.0.1:4998"

	data = {
	"message": "ping",
	"chatid": "1234",
	"frontend": "chatpage"
	}

	response = requests.post(url, json=data)

	print(response.text)

	return "jsonify(messagejson)"

'''
@app.route('/long_poll')
def long_poll():
	try:
		while True:
			response = requests.get('http://127.0.0.1:5000/msg')  
			data = response.text
			print("Received data:", data)
			time.sleep(1) 
	except requests.exceptions.RequestException as e:
		print("Error:", e)
		time.sleep(10)
		long_poll()
'''
if __name__ == '__main__':
	app.run(debug=True, threaded=True, port=5000)
