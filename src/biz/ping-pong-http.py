import http.server
import socketserver
import http.client
import json
from urllib.parse import parse_qs, urlencode
import requests
import http.client


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""

def frontend_url(frontend):
	if frontend == "frontest":
		return "http://localhost:4999"
	elif frontend == "mercadolibre":
		return "https://meli.goldenwordai.com:5000/vuelta"
	elif frontend == "chatpage":
		return "https://pingpong.test.goldenwordai.com:5000/vuelta"
	elif frontend == "react":
		return "http://bff.test.goldenwordai.com:6060/message/sendForApi"
	elif frontend == "fronttest":
		return "https://pingpong.test.goldenwordai.com:4999/vuelta"
	elif frontend == "telegram":
		return "http://ssh.telegrama.test.pokerbuddyai.com:10302/outbound"
	else:
		return "No frontend url", 400

def jsonrequest(self, message, frontend, chatid):
	response_data = {"message": "Sending response to " + frontend_url(frontend), "response": message, "chatid": chatid}
	response_json = json.dumps(response_data)
	self.wfile.write(response_json.encode())
	print("Send response to " + frontend_url(frontend))

def sendResponse (message, frontend, chatid):
			headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
			}
			payload = urlencode({
				'response': message,
				'chatid': chatid
			})
			response = requests.request("POST", frontend_url(frontend), headers=headers, data=payload)
			print(response.text)

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.wfile.write(b"PingPong HTTP Server. Running port 4998")

	def do_POST(self):
		content_length = int(self.headers["Content-Length"])
		post_data = self.rfile.read(content_length).decode()
  
		if self.headers['Content-Type'] == "application/json":
			post_data = json.loads(post_data)
			message = post_data['message']
			chatid = post_data['chatid']
			frontend = post_data['frontend']
		elif self.headers['Content-Type'] == "application/x-www-form-urlencoded":
			post_data = parse_qs(post_data)
			message = post_data['message'][0]
			chatid = post_data['chatid'][0]
			frontend = post_data['frontend'][0]
		
		print ("Received:" +  str(post_data))

		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()

		if message.lower() == "ping":
			try:
				sendResponse("pong", frontend, chatid)
				jsonrequest(self,"pong", frontend, chatid)
				
			except Exception as e:
				self.wfile.write((json.dumps({"error": str(e)})).encode())

		else:
			# error generico
			sendResponse("No pong", frontend, chatid)
			jsonrequest(self,"No pong", frontend, chatid)

			# error especifico
			sendResponse("input was " + message.lower(), frontend, chatid)
			jsonrequest(self,"input was " + message.lower(), frontend, chatid)

if __name__ == "__main__":
	server_address = ("0.0.0.0", 4998)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()
