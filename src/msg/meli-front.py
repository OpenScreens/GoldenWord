import http.server
import os
import urllib.parse
import socketserver
import http.client
import json
import time
from datetime import datetime, timezone, timedelta

fecha_hora_actual = datetime.now(timezone.utc)
path = "timeauth.txt"

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
		if self.path == "/":
			self.send_response(404)
			self.end_headers()
		if self.path == '/notification':
			print("Received POST request")
			self.send_header('Content-type', 'application/json')
			self.send_header('Connection', 'close')
			self.send_response(200)
			self.end_headers()

			content_length = int(self.headers['Content-Length'])
			post_data = self.rfile.read(content_length)
			post_params = urllib.parse.parse_qs(post_data)

			data = post_data.decode('utf-8')
			print("Notification received:")
			print(data)
			decoded_data = json.loads(data)
			resource = decoded_data.get('resource')
	
			ti_m = os.path.getmtime(path)
			timefile = datetime.utcfromtimestamp(ti_m)
			timefile = timefile.replace(tzinfo=timezone.utc)
			diferencia_tiempo = fecha_hora_actual - timefile
			min_time = timedelta(hours=6)
			conn = http.client.HTTPSConnection("api.mercadolibre.com")
   
			if diferencia_tiempo >= min_time:

				print("Han pasado al menos 6 horas. Se realiza el post." + str(timefile) + str(fecha_hora_actual))
				payload = 'grant_type=refresh_token&client_id=7875887431713058&client_secret=SZU8d3beJhUAJnw3ezsZflgtD6w3JpLD&refresh_token=TG-65f83a97c20ab30001f99f40-1726462588'
				headers = {
				'accept': 'application/json',
				'content-type': 'application/x-www-form-urlencoded'
				}
				conn.request("POST", "/oauth/token", payload, headers)
				res = conn.getresponse()
				data = res.read().decode("utf-8")
				response_data = json.loads(data)
				meli_tokenn = response_data.get('access_token')
				with open("timeauth.txt", "w") as f:
					f.write(str(meli_tokenn))
			else:
				print("Aún no han pasado 6 horas desde el timestamp. No se realiza ninguna acción " + str(timefile) + str(fecha_hora_actual))

			with open('timeauth.txt', 'r') as f:
				lines = f.readlines()
				meli_token = lines[-1]
   
			#Open connection to MercadoLibre
			headers = {
				'Authorization': f'Bearer {meli_token}'
			}

			#Get unread messages
			conn.request("GET", f"/messages/{resource}?tag=post_sale", headers=headers)
			res = conn.getresponse()
			data = res.read()
			data_message = json.loads(data)
			messageGET = (data_message['messages'][0]['text']).replace("\n", "")
			userfrom = (data_message['messages'][0]['from']['user_id'])
			userto = data_message['messages'][0]['to']['user_id']
			idpack = data_message['messages'][0]['message_resources'][0]['id']

			print("###1 Message received: " + messageGET)

			
			messagejson=[{
				"message": messageGET,
				"from": userfrom,
				"to": userto,
				"chatid": idpack,
				"frontend": "mercadolibre"
			}]
			print(messagejson)
			body = json.dumps(messagejson)
			headers = {
			'Content-Type': 'application/json'
			}
			backend = http.client.HTTPSConnection("pingpong.test.goldenwordai.com", 4998)
			backend.request("POST", "/", body, headers)
			resv = backend.getresponse()
			datav = resv.read().decode("utf-8")
			if (resv.status == 200):
				print("PingPong 200")
			else:
				print("Problem server pingpong" + str(resv.status))
				return;

		#def vuelta(self)
		elif self.path == '/vuelta':
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			content_length = int(self.headers['Content-Length'])
			post_data = self.rfile.read(content_length)
			post_params = urllib.parse.parse_qs(post_data.decode("utf-8"))
			resource = post_params.get('response', [''])[0]
			print("###rst pingpong: " + str(post_params))
			payload = json.dumps({
				"from": {
					"user_id": userto
				},
				"to": {
					"user_id": userfrom
				},
				"text": str(resource)
			})
		
			headers['Content-Type'] = 'application/json'
			conn.request("POST", f"/messages/packs/{idpack}/sellers/{userto}?tag=post_sale", payload, headers)
			resv = conn.getresponse()
			datav = resv.read().decode("utf-8")
			conn.close()

if __name__ == '__main__':
	server_address = ('0.0.0.0', 5000)
	httpd = ThreadedHTTPServer(server_address, SimpleHTTPRequestHandler)
	print("Serving HTTP on port 5000..")
	httpd.serve_forever()
