import http.server
import socketserver
import http.client
import json
import urllib
from urllib import request
from urllib.parse import parse_qs, urlencode
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
		return "http://bff.test.goldenwordai.com"
	else:
		return "No frontend url", 400
		
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(b'PingPong HTTP Server. Running port 4998')

	def do_POST(self):
		'''content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length).decode('utf-8')
		decoded_data = parse_qs(post_data)
  
		message = decoded_data.get('message', ['nonedefault'])[0]
		chatid = decoded_data.get('chatid', ['nonedefault'])[0]
		frontend = decoded_data.get('frontend', ['nonedefault'])[0]
		userto = decoded_data.get('to', ['nonedefault'])[0]
		userfrom = decoded_data.get('from', ['nonedefault'])[0]'''
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
  
		if message.lower() == "ping":
			print("Pong")
			requests.post(frontend_url(frontend), urlencode({"response": "pong", "chatid": chatid}))

		else:
			#error generico
			requests.post(frontend_url(frontend), urlencode({"response": "error", "chatid": chatid}))

			#error especifico
			requests.post(frontend_url(frontend), urlencode({"response": "input was " + message.lower(), "chatid": chatid}))

if __name__ == '__main__':
	server_address = ('0.0.0.0', 4998)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()
