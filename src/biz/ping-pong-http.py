import http.server
import socketserver
import http.client
import json

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(b'Running port 5000')

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		post_data = json.loads(post_data.decode())
		
		message = post_data.get('message', ['nonedefault'])
		chatid = post_data.get('chatid', ['nonedefault'])
		frontend = post_data.get('frontend', ['nonedefault'])
		userto = post_data.get('to', ['nonedefault'])
		userfrom = post_data.get('from', ['nonedefault'])
		print (message)
		
		if message.lower() == "ping":
			print("Pong")
			response_data = {"response": "pong", "chatid": chatid}
		else:
			response_data = {"response": "error", "chatid": chatid}
		
		encoded_response_data = "&".join([f"{key}={value}" for key, value in response_data.items()])
		
		self.send_response(200)
		self.send_header('Content-type', 'application/x-www-form-urlencoded')
		self.end_headers()
		self.wfile.write(encoded_response_data.encode())

if __name__ == '__main__':
	server_address = ('0.0.0.0', 4998)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()
