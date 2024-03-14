import http.server
import requests
import urllib.parse
backend_url = "http://localhost:4998/new_message"



def send_msg(msg,chatid):
	requests.post(backend_url,{"message":msg,"chatid":chatid,"frontend":"Frontest"},headers={"content-encoding":"multipart/form-data"})
send_msg("inbound msg1","1")
#send_msg("inbound msg2","2")

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_POST(self):
		print("received post")
		# This function handles GET requests
		# Send response status code
		self.send_response(200)
		# Send headers
		self.send_header('Content-type', 'application/x-www-form-urlencoded')
		self.end_headers()
		content_length = int(self.headers['Content-Length'])
		# Read and decode the request body
		post_data = self.rfile.read(content_length).decode('utf-8')
		# Assuming the content type is application/x-www-form-urlencoded
		# Parse the query string into a dictionary
		post_params = urllib.parse.parse_qs(post_data)
		# Send the response content
		response_content = b"Received response. Sending to messaging app."
		self.wfile.write(response_content)
		# Post-response processing: Log something to a file
		print(post_params)
		chatid = post_params["chatid"][0]
		message = post_params["response"][0]
		with open("chat"+chatid+".txt", "a") as chat_file:
			chat_file.write(message+"\r\n")

if __name__ == '__main__':
	server_address = ('0.0.0.0', 4999)  # Serve on all addresses, port 4999
	httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4999..")
	httpd.serve_forever()

