import http.server
import urllib.parse
import socketserver
import json

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    stored_json = None

    def do_GET(self):
        if self.path == '/getjson':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if self.stored_json:
                self.wfile.write(json.dumps(self.stored_json).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"message": "No hay datos almacenados"}).encode('utf-8'))

    def do_POST(self):
        print("Received POST request")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = post_data.decode('utf-8')
        print("JSON received:")
        json_data = json.loads(data)
        print(json_data)
        CustomHTTPHandler.stored_json = json_data
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Received JSON')

if __name__ == '__main__':
    server_address = ('0.0.0.0', 5000)
    httpd = ThreadedHTTPServer(server_address, CustomHTTPHandler)
    print("Serving HTTP on port 5000..")
    httpd.serve_forever()
