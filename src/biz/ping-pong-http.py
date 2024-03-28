import http.server
import socketserver
import http.client
import json

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""


def frontend_url(frontend):
	if frontend == "chatpage":
		return "http://localhost:5000"
	if frontend == "meli":
		return "blablabla"
		
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
		
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.send_header('Content-Length', '0')
		self.end_headers()

		header= {'Content-Type':'application/x-www-form-urlencoded'}
		if message.lower() == "ping":
			print("Pong")
			requests.post(frontend_url(frontend),{"response": "pong", "chatid": chatid})
		else:
			#error generico
			requests.post(frontend_url(frontend),{"response": "error", "chatid": chatid},)
			#error especifico
			requests.post(frontend_url(frontend),{"response": "input was "+ messsage.lower(), "chatid": chatid},)
		


if __name__ == '__main__':
	server_address = ('0.0.0.0', 4998)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()
