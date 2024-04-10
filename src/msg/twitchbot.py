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
		'''if self.path == "/":
			self.send_response(404)
			self.end_headers()'''
		if self.path == '/callback':
			content_length = int(self.headers["Content-Length"])
			post_data = self.rfile.read(content_length).decode()
			post_data = json.loads(post_data)
			print("Received POST TWITCH")
			print(post_data)
			self.send_header('Content-type', 'application/json')
			self.send_header('Connection', 'close')
			self.send_response(200)
			self.end_headers()

			'''
   			content_length = int(self.headers['Content-Length'])
			post_data = self.rfile.read(content_length)
			post_params = urllib.parse.parse_qs(post_data)

			data = post_data.decode('utf-8')
			print("Notification received:")
			print(data)
			'''
			# enviarmessage("ping")
			# enviarmessage("pong")

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
