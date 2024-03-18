import http.server
import urllib.parse
import socketserver
import http.client
import json
import time

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/':
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write(b'Mercado Libre BOT running')

	def do_POST(self):
		print("Received POST request")
		self.send_header('Content-type', 'application/json')
		self.send_header('Connection', 'close')
		self.send_response(200)
		self.end_headers()

		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		post_params = urllib.parse.parse_qs(post_data)

		decoded_data = post_data.decode('utf-8')
		print("Notification received:")
		print(decoded_data)
		time.sleep(7)

		#Open connection to MercadoLibre
		conn = http.client.HTTPSConnection("api.mercadolibre.com")
		headers = {
			'Authorization': 'Bearer APP_USR-7875887431713058-031816-1c3bc3a915779f270165a76749cf0fa5-1726462588'
		}

		try:
			#Get unread messages
			conn.request("GET", f"/messages/{decoded_data['resource']}?tag=post_sale", headers=headers)
			res = conn.getresponse()
			data = res.read()
			data_message = json.loads(data)
			messageGET = (data_message['messages'][0]['text']).replace("\n", "")
			userfrom = (data_message['messages'][0]['from']['user_id'])
			userto = data_message['messages'][0]['to']['user_id']
			idpack = data_message['messages'][0]['message_resources']['id']
   
			print("###1 Message received: " + messageGET)
   
			messagejson=[{
				"message": messageGET,
				"from": userfrom,
				"to": userto,
				"idpack": idpack  
			}]
   
			body = json.dumps(messagejson)
			backend = http.client.HTTPSConnection("meli.goldenwordai.com", 4999)
			backend.request("POST", "/", body, headers)
			resv = backend.getresponse()
			datav = resv.read().decode("utf-8")
			print(datav)  # Imprime la respuesta del servidor   
   
		except (http.client.HTTPException, json.decoder.JSONDecodeError) as e:
			print(f"Error: {e}")
		finally:
			conn.close()
			return;

if __name__ == '__main__':
	server_address = ('0.0.0.0', 5000)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 5000..")
	httpd.serve_forever()
