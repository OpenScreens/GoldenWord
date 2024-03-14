import flask
import threading
import requests

app = flask.Flask(__name__)
front_url = "http://localhost:4999/back_to_front"

@app.route('/new_message',methods=["POST"])
def receive_msg():
    print(flask.request.form)
    msg = flask.request.form.get("message")
    chatid = flask.request.form.get("chatid")
    print("chatid is: " + str(chatid))
    frontend = flask.request.form.get("frontend")
    print("Got message: " + str(msg))
    threading.Thread(target=process_msg, args=(msg,chatid,frontend)).start()
    return "ok. Telegram test backend received input."

def process_msg(msg,chatid,frontend):
    #response = msg
    #response = "Response from backend"
	respond_msg("thinking",chatid,frontend)
	response = process_inbound_message(msg)
	respond_msg(response,chatid,frontend)

def respond_msg(response,chatid,frontend):
    if frontend == "telegram":
	#sending output response.
        requests.post(front_url,data={"response":response,"chatid":chatid})



def process_inbound_message(msg):
	if msg.strip().lower() == "ping":
		return "pong"
	else:
		return "error"

app.run(host='0.0.0.0', port=4998)
