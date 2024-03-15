import flask
import requests
app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	message = flask.request.form.get('message')
	chatid = flask.request.form.get('chatid')
	frontend = flask.request.form.get('frontend')
	
	if frontend.strip().lower() == "frontest":
		frontend_url = "http://localhost:4999"
	else:
		raise Exception("frontend not recognized")
	if message.lower() == "ping":
		print("Pong")
		requests.post(frontend_url,{"response":"pong","chatid":chatid},headers={"content-encoding":"application/x-www-form-urlencoded"})
		requests.post(frontend_url,{"response":"pong2","chatid":chatid},headers={"content-encoding":"application/x-www-form-urlencoded"})
		return "Received message and sent response."

	else:
		requests.post(frontend_url,{"response":"error","chatid":chatid},headers={"content-encoding":"application/x-www-form-urlencoded"})
		return "Received message and sent response."
if __name__ == '__main__':
	app.run('0.0.0.0','4998',debug=True)
