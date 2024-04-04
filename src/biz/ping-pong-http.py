import http.server
import socketserver
import http.client
import json
from urllib.parse import urlencode, parse_qs
import requests

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
		return "http://bff.test.goldenwordai.com:6000"
	elif frontend=="backtest":
		return "http://localhost:5000/test"
	elif frontend=="telegram":
		return "http://ssh.telegrama.test.pokerbuddyai.com:10302"
	else:
		return "No frontend url", 400
		
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(b'PingPong HTTP Server. Running port 4998')

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		if self.headers['Content-Type'] == "application/json":
			post_data = json.loads(post_data.decode())
		elif self.headers['Content-Type'] == "application/x-www-form-urlencoded":
			post_data = parse_qs(post_data.decode())
		message = post_data.get('message', ['default'])
		chatid = post_data.get('chatid', ['default'])
		frontend = post_data.get('frontend', ['default'])
  
		print ("Received json:" +  str(post_data))
		
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.send_header('Content-Length', '0')
		self.end_headers()
  
		if message.lower() == "ping":
			requests.post(frontend_url(frontend), urlencode({"response": "pong", "chatid": chatid}))
			print("Send response ping to " + frontend_url(frontend))

		else:
			#error generico
			requests.post(frontend_url(frontend), urlencode({"response": "No Pong", "chatid": chatid}))

			#error especifico
			requests.post(frontend_url(frontend), urlencode({"response": "input was " + message.lower(), "chatid": chatid}))
			print("Send error response to " + frontend_url(frontend))

if __name__ == '__main__':
	server_address = ('0.0.0.0', 4998)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()
