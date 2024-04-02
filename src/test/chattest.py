from flask import jsonify, request
from urllib.parse import parse_qs
from flask import Flask
import requests

inputMessage = ["ping","hola",'}e%$>"&/p}']
outputExpected = ["pong", 'No Pong', 'input was holal', 'No Pong', 'input was }e%$>"&/p}']
outputr = []

app = Flask(__name__)

def test_send_message(input_msg):
    url = "http://localhost:4998/"
    data = {"message": input_msg, "chatid": "123", "frontend": "backtest"}
    requests.post(url, json=data, timeout=10)
    print(f"sending message '{input_msg}'")

@app.route('/testinput')
def send_test_messages():
    for message in inputMessage:
        test_send_message(message)
    return jsonify({'message': 'Pruebas de envío de mensajes realizadas con éxito'})

@app.route('/test', methods=['POST','GET'])
def do_post():
	global outputr
	if request.method == 'POST':
		post_data = request.data.decode('utf-8')
		decoded_data = parse_qs(post_data)
		response = decoded_data.get('response', [''])[0]
		print("response: " + response)
		outputr.append(response)
		print(outputr)
  
	if len(outputr) == len(outputExpected):
		print(outputExpected)
		try:
			for i in range(len(outputExpected)):
				assert outputr[i] == outputExpected[i], f"Error: respuesta recibida {outputr[i]}, esperada {outputExpected[i]}"
		except AssertionError as e:
			error_message = str(e)
			print(error_message)
			return jsonify({'error': error_message})
		finally:
			outputr = []
	return jsonify({'message':'Esperando respuestas'})

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)



