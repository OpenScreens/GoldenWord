import http.server
import socketserver
import http.client
import json
import urllib
import requests

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""


def frontend_url(frontend):
	if frontend == "frontest":
		return "http://localhost:4999"
	elif frontend == "mercadolibre":
		return "https://meli.goldenwordai.com:5000/vuelta"
	elif frontend == "chatpage":
		return "http://localhost:5000/"
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
			query_string = urllib.parse.urlencode({"response": "pong", "chatid": chatid})
			requests.post(frontend_url(frontend),data=query_string)
		else:
			#error generico
			query_string = urllib.parse.urlencode({"response": "error", "chatid": chatid})
			requests.post(frontend_url(frontend),data=query_string)

			#error especifico
			query_string = urllib.parse.urlencode({"response": "input was " + message.lower(), "chatid": chatid})
			requests.post(frontend_url(frontend),data=query_string)

if __name__ == '__main__':
	server_address = ('0.0.0.0', 4998)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()
