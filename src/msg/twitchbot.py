import http.server
import socketserver
import http.client
import json

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/':
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write(b'twitch BOT running')

	def do_POST(self):
		if self.path == '/callback':
			content_length = int(self.headers["Content-Length"])
			post_data = self.rfile.read(content_length).decode()
			post_data = json.loads(post_data)
			print("Received POST TWITCH")
			print(post_data)
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.send_header('Connection', 'close')
			self.end_headers()

			if 'type' in post_data:
				if post_data['type'] == 'webhook_callback_verification':
					self.wfile.write(post_data['challenge'].encode())
				elif post_data['type'] == 'notification':
					handle_notification(post_data)
				elif post_data['type'] == 'revocation':
					handle_revocation(post_data)
			else:
				print("Unknown message type")

def handle_notification(notification):
	print("Notification received:")
	print(json.dumps(notification, indent=4))

def handle_revocation(revocation):
	print("Revocation received:")
	print(json.dumps(revocation, indent=4))

def enviarmessage(message):
	conn = http.client.HTTPSConnection("api.twitch.tv")
	payload = json.dumps({
	"broadcaster_id": "1063475030",
	"sender_id": "1063475030",
	"message": message
	})
	headers = {
	'Content-Type': 'application/json',
	'Authorization': 'Bearer x9toyqcnjp7efn3abm2ugjaqbhd8x7',
	'Client-Id': 'pfmyo3749gxj2yyatlsjwazrr5zhzn',
	'Content-Type': 'application/json'
	}
	conn.request("POST", "/helix/chat/messages", payload, headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))

if __name__ == '__main__':
	server_address = ('0.0.0.0', 5000)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 5000..")
	httpd.serve_forever()
