import threading
import time
import http.server
import socketserver
import http.client
import json
from urllib.parse import parse_qs, urlencode
import requests
import http.client
from requests_oauthlib import OAuth1Session
import os
import json

##Hide on production
consumer_key = "BwkR1mbGBzyQc8Nxxkw5eXwEf"
consumer_secret = "xpZhCKac6j9HzGa2lUCYm8XR3MviFkepi4uVJoVa2NRFV2GlE6"
access_token = "1803163556797460480-8wl1gSo5T183R2bfqx18CrEs9xReFr"
access_token_secret = "ZcD5CHQzqyUnlqMbiaBDGsZNWI9rXJafmnU7goEBNUFZ4"
##


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		sendResponse()
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.wfile.write(b"TwitterBOT HTTP Server. Running port 80")

	def do_POST(self):
		content_length = int(self.headers["Content-Length"])
		post_data = self.rfile.read(content_length).decode()
		print ("Received:" +  str(post_data))
	
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
		
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.send_header("Content-Length","0")
		self.end_headers()



def sendResponse():
	#textinput = input("Tweet: ")
	payload = {"text": 'test'}
	print("test tweet")

	oauth = OAuth1Session(
		consumer_key,
		client_secret=consumer_secret,
		resource_owner_key=access_token,
		resource_owner_secret=access_token_secret,
	)

	response = oauth.post("https://api.x.com/2/tweets",json=payload,)

	if response.status_code != 201:
		raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

	print("Response code: {}".format(response.status_code))

	json_response = response.json()
	print(json.dumps(json_response))
 
 

if __name__ == "__main__":
	server_address = ("0.0.0.0", 80)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 80..")
	httpd.serve_forever()
