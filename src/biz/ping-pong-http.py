import threading
import time
import http.server
import socketserver
import http.client
import json
from urllib.parse import parse_qs, urlencode
import requests
import http.client

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""

def frontend_urls(frontend):
	urls = []
	if frontend == "frontest":
		urls.append("http://localhost:4999")
	elif frontend == "mercadolibre":
		urls.append("https://meli.goldenwordai.com:5000/vuelta")
	elif frontend == "chatpage":
		urls.append("https://pingpong.test.goldenwordai.com:5000/vuelta")
	elif frontend == "react3":
		urls.append("http://react.test.pokerbuddyai.com:6060/message/sendForApi")
	elif frontend == "fronttest":
		urls.append("http://chatping.test.goldenwordai.com/vuelta")
		urls.append("http://chatping.test.goldenwordai.com/heart")
	elif frontend == "twitter":
		urls.append("http://twitterbot.test.goldenwordai.com/response")
		urls.append("http://twitterbot.test.goldenwordai.com/heart")
	elif frontend == "telegram":
		urls.append("http://ssh.telegrama.test.pokerbuddyai.com:10302/outbound")
	elif frontend == "chathelp":
		urls.append("http://localhost/response")
		urls.append("http://localhost/heart")
	else:
		return "No frontend url", 400
	return urls

def send_response(message, frontends, user_id, chat_id):
			headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
			}
			payload = urlencode({
				'response': message,
				'user_id': user_id,
				'chat_id': chat_id,
				'source': 'i made it up'
			})
			response = requests.request("POST", frontends, headers=headers, data=payload)
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
			user_id = post_data['user_id']
			chat_id = post_data['chat_id']
			frontend = post_data['frontend']
		elif self.headers['Content-Type'] == "application/x-www-form-urlencoded":
			post_data = parse_qs(post_data)
			message = post_data['message'][0]
			user_id = post_data['user_id'][0]
			chat_id = post_data['chat_id'][0]
			frontend = post_data['frontend'][0]
		
		print ("Received:" +  str(post_data))

		heartbeat_thread = HeartbeatThread(frontend_urls(frontend)[1], user_id, chat_id)
		heartbeat_thread.start()

		response_message = ""
		if message.lower() == "ping":
			try:
				heartbeat_thread.stop()
				response_message = "pong"
			except Exception as e:
				response_message = json.dumps({"error": str(e)})
		else:
			heartbeat_thread.stop()
			response_message = f"No pong. Input was {message.lower()}"

		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
		self.end_headers()
		
		response_data = {
			"response": response_message,
			"user_id": user_id,
			"chat_id": chat_id,
			"source": "i made it up"
		}
		self.wfile.write(json.dumps(response_data).encode())
		send_response(response_message, frontend_urls(frontend)[0], user_id, chat_id)

	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
		self.end_headers()

class HeartbeatThread(threading.Thread):
	def __init__(self, frontends, user_id, chat_id):
		threading.Thread.__init__(self)
		self.frontends = frontends
		self.user_id = user_id
		self.chat_id = chat_id
		self.stop_event = threading.Event()

	def run(self):
		while not self.stop_event.is_set():
			try:
				send_response("Working", self.frontends, self.user_id, self.chat_id)
			except Exception as e:
				print("Error sending heartbeat:", str(e))
			time.sleep(0.3)

	def stop(self):
		self.stop_event.set()

if __name__ == "__main__":
	server_address = ("0.0.0.0", 4998)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()
