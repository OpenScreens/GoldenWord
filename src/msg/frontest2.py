import requests
backend_url = "http://localhost:4998/"

def send_msg(msg,chatid):
        print("sending")
        requests.post(backend_url,{"message":msg,"chatid":chatid,"frontend":"Frontest"},headers={"content-encoding":"multipart/form-data"})
        print("sent")
send_msg("inbound msg1","1")
#send_msg("inbound msg2","2")
