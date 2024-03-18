import http.server
import urllib.parse
import socketserver
import ssl

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_POST(self):
		print("received post")
		self.send_response(200)
  
		# Send headers
		self.send_header('Content-type', 'application/x-www-form-urlencoded')
		self.send_header('Connection', 'close')
		content_length = int(self.headers['Content-Length'])
  
		# Read and decode the request body
		post_data = self.rfile.read(content_length).decode('utf-8')
		# Assuming the content type is application/x-www-form-urlencoded
		# Parse the query string into a dictionary
		post_params = urllib.parse.parse_qs(post_data)
		# Send the response content
		response_content = b"Received response. Sending to messaging app."
		self.send_header("Content-length",len(response_content))
		self.end_headers()

		self.wfile.write(response_content)
		# Post-response processing: Log something to a file
		print(post_params)
  
		# resourceid = post_params["_id"][0]
		# print (resourceid)
  
		# conn = http.client.HTTPSConnection("api.mercadolibre.com")
		# payload = ''
		# headers = {
		# 'Authorization': 'Bearer APP_USR-3866013582804370-031511-3958dd20424e5e5c8e00d8a378bc39e0-1726462588'
		# }
		# conn.request("GET", f"/messages/{resourceid}", payload, headers)
		# res = conn.getresponse()
		# data = res.read()
		# print(data.decode("utf-8"))
  
		# with open("chat"+chatid+".txt", "a") as chat_file:
		# 	chat_file.write(message+"\r\n")

# if __name__ == '__main__':
# 	server_address = ('0.0.0.0', 5000)  
# 	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
# 	httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='key.pem', certfile='cert.pem', server_side=True)
# 	print("Serving HTTPS on port 5000..")
# 	httpd.serve_forever()

if __name__ == '__main__':
	server_address = ('0.0.0.0', 5000)  # Serve on all addresses, port 5000
	httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 5000..")
	httpd.serve_forever()
