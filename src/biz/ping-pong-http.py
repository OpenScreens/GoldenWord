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
	elif frontend == "react3":
		return "http://react.test.pokerbuddyai.com:6060/message/sendForApi"
	elif frontend == "fronttest":
		return "http://chatping.test.goldenwordai.com/vuelta"
	elif frontend == "telegram":
		return "http://ssh.telegrama.test.pokerbuddyai.com:10302/outbound"
	else:
		return "No frontend url", 400

def sendResponse (message, frontend, userid, chatid):
			headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
			}
			payload = urlencode({
				'response': message,
				'userid': userid,
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
			userid = post_data['userid']
			chatid = post_data['chatid']
			frontend = post_data['frontend']
		elif self.headers['Content-Type'] == "application/x-www-form-urlencoded":
			post_data = parse_qs(post_data)
			message = post_data['message'][0]
			userid = post_data['userid'][0]
			chatid = post_data['chatid'][0]
			frontend = post_data['frontend'][0]
		
		print ("Received:" +  str(post_data))

		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.send_header("Content-Length","0")
		self.end_headers()

		if message.lower() == "ping":
			try:
				sendResponse("pong", frontend, userid, chatid)
				
			except Exception as e:
				self.wfile.write((json.dumps({"error": str(e)})).encode())

		else:
			# error generico
			sendResponse("No pong", frontend, userid, chatid)

			# error especifico
			sendResponse("input was " + message.lower(), frontend, userid, chatid)

if __name__ == "__main__":
	server_address = ("0.0.0.0", 4998)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()
