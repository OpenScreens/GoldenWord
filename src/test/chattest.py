import os
import signal
import time
from flask import jsonify, request
from urllib.parse import parse_qs
from flask import Flask
import requests

inputMessage = ["ping","hola",'}e%$>"&/p}']
outputExpected = ["pong", 'No Pong', 'input was hola', 'No Pong', 'input was }e%$>"&/p}']
outputr = []
testresults = []
test_names = ["test1", "test2", "test3", "test4", "test5"]

app = Flask(__name__)

def test_send_message(input_msg):
    url = "http://localhost:4998/"
    data = {"message": input_msg, "chatid": "123", "frontend": "backtest"}
    requests.post(url, json=data, timeout=10)

@app.route('/testinput')
def send_test_messages():
	for message in inputMessage:
		test_send_message(message)
		time.sleep(3)
	return jsonify({'message': 'Pruebas de envío de mensajes realizadas con éxito'})

@app.route('/test', methods=['POST','GET'])
def do_post():
	global outputr
	if request.method == 'POST':
		post_data = request.data.decode('utf-8')
		decoded_data = parse_qs(post_data)
		response = decoded_data.get('response', [''])[0]
		outputr.append(response)

	if len(outputr) == len(outputExpected):
		print(outputExpected)
		try:
			for i in range(len(outputExpected)):
				if outputExpected[i]==outputr[i]:
					testresults.append("pass")
				elif outputExpected[i]!=outputr[i]:
					testresults.append("fail")
		finally:
			print (outputExpected)
			print (outputr)
			outputr = []
			result_dict = {test_names[i]: testresults[i] for i in range(len(test_names))}
			print (result_dict)
			os.kill(os.getpid(), signal.SIGTERM)
   
	return jsonify({'message':'Esperando respuestas'})
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)
