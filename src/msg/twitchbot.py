import http.server
import socketserver
import http.client

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
			print("Received POST TWITCH")
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
   
if __name__ == '__main__':
	server_address = ('0.0.0.0', 443)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 443..")
	httpd.serve_forever()
