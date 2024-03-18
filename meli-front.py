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
			conn.request("GET", "/messages/unread?role=seller&tag=post_sale", headers=headers)
			res = conn.getresponse()
			data = res.read()
			datar = json.loads(data)
			print(datar['results'][0]['resource'])

			#Get message by id
			conn.request("GET", f"/messages{datar['results'][0]['resource']}?tag=post_sale", headers=headers)
			res = conn.getresponse()
			data = res.read()
			datarr = json.loads(data)
			message = datarr['messages'][0]['text']
			print(message)
			
			#if message is ping respond with pong
			if (message == "ping"):
				payload = json.dumps({
					"from": {
						"user_id": 1726462588
					},
					"to": {
						"user_id": 1724090395
					},
					"text": "Pong"
				})
			else:
				payload = json.dumps({
					"from": {
						"user_id": 1726462588
					},
					"to": {
						"user_id": 1724090395
					},
					"text": "Error"
				})	

			headers['Content-Type'] = 'application/json'
			conn.request("POST", f"/messages{datar['results'][0]['resource']}?tag=post_sale", payload, headers)
			resv = conn.getresponse()
			datav = resv.read().decode("utf-8")

			payload = ''
			conn.request("GET", "/messages/packs/2000007820894242/sellers/1726462588?tag=post_sale", payload, headers)
			resl = conn.getresponse()
			datal = resl.read().decode("utf-8")
   
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
