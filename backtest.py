import http.server
import requests
import urllib.parse
import socketserver
front_url = "http://localhost:4999"



def process_msg(msg,chatid,frontend):
    #response = msg
    #response = "Response from backend"
        respond_msg("thinking",chatid,frontend)
        response = process_inbound_message(msg)
        respond_msg(response,chatid,frontend)
	
def respond_msg(response,chatid,frontend):
	requests.post(front_url,data={"response":response,"chatid":chatid})



def process_inbound_message(msg):
        if msg.strip().lower() == "ping":
                return "pong"
        else:
                return "error"
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	#/new_message
	def do_POST(self):
		print("received post")
		# This function handles GET requests
		# Send response status code
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
		response_content = b"Received message. Sending to backend app."
		self.send_header("Content-length",len(response_content))
		self.end_headers()

		self.wfile.write(response_content)
		# Post-response processing: Log something to a file
		print(post_params)
		chatid = post_params["chatid"][0]
		message = post_params["message"][0]
		process_msg(message,chatid,"frontend")

if __name__ == '__main__':
	server_address = ('127.0.0.1', 4998)  # Serve on all addresses, port 4999
	httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 4998..")
	httpd.serve_forever()

