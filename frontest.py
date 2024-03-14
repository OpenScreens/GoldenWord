import flask
import threading
import requests

app = flask.Flask(__name__)
backend_url = "http://localhost:4998/new_message"


@app.route('/mock_receive',methods=["GET"])
def mock_receive():
	threading.Thread(target=send_msg,args=("inbound msg1","1")).start()
	threading.Thread(target=send_msg,args=("inbound msg2","2")).start()
	return "ok. receiving 2 mock messages."

@app.route('/mock_receive_params',methods=["POST"])
def mock_receive_params():
	msg1 = flask.request.form.get("msg1")
	msg2 = flask.request.form.get("msg2")

	threading.Thread(target=send_msg,args=("msg1","1")).start()
	threading.Thread(target=send_msg,args=("msg2","2")).start()
	return "ok. receiving 2 mock messages."

def send_msg(msg,chatid):
	requests.post(backend_url,{"message":msg,"chatid":chatid,"frontend":"Frontest"},headers={"content-encoding":"multipart/form-data"})

@app.route("/back_to_front",methods=["POST"])
def returning_msg(msg,chatid):
	f = open("chat"+chatid+".txt","a")
	f.write(msg+"\r\n")
	f.close()

app.run(host='0.0.0.0', port=4999)
