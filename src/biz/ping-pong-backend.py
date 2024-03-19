import flask
import requests
app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	message = flask.request.form.get('message','nonedefault')
	chatid = flask.request.form.get('chatid','nonedefault')
	frontend = flask.request.form.get('frontend', 'nonedefault')
	userto = flask.request.form.get('to', 'nonedefault')
	userfrom = flask.request.form.get('from', 'nonedefault')

	if frontend.strip().lower() == "frontest":
		frontend_url = "http://localhost:4999"
	if frontend.strip().lower() == "mercadolibre":
		frontend_url = "https://meli.goldenwordai.com:5000/vuelta"	
	
	if message.lower() == "ping":
		print("Pong")
		requests.post(frontend_url,{"response":"pong","chatid":chatid},headers={"content-encoding":"application/x-www-form-urlencoded"})
		return "Received message and sent response."

	else:
		requests.post(frontend_url,{"response":"error","chatid":chatid},headers={"content-encoding":"application/x-www-form-urlencoded"})
		return "Received message and sent response."

if __name__ == '__main__':
	app.run('0.0.0.0','4998',debug=True)
