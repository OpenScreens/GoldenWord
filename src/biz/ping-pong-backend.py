import flask
import requests
app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	json_data = flask.request.json
	message = json_data.get('message', 'nonedefault')
	chatid = json_data.get('chatid', 'nonedefault')
	frontend = json_data.get('frontend', 'nonedefault')
	userto = json_data.get('to', 'nonedefault')
	userfrom = json_data.get('from', 'nonedefault')
	#print(json_data)

	if frontend.strip().lower() == "frontest":
		frontend_url = "http://localhost:4999"
	elif frontend.strip().lower() == "mercadolibre":
		frontend_url = "https://meli.goldenwordai.com:5000/vuelta"
	elif frontend == "chatpage":
		frontend_url = "http://localhost:5000/"
	else:
		return "No frontend url", 400
	
	if message.lower() == "ping":
		print("Pong")
		response_data = {"response": "pong", "chatid": chatid}
	else:
		response_data = {"response": "error", "chatid": chatid}

	encoded_response_data = "&".join([f"{key}={value}" for key, value in response_data.items()])

	return encoded_response_data, 200, {'Content-Type': 'application/x-www-form-urlencoded'}

if __name__ == '__main__':
	app.run('0.0.0.0','4998',debug=True)
