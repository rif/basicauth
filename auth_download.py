import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)
        user, passw = '', ''
        if 'user' in query_components:
            user = query_components["user"][0]
        if 'pass' in query_components:
            passw = query_components["pass"][0]
        if user != 'adi' or passw != 'test':
            self.send_response(403)
            self.end_headers()
            return

        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the headers
        self.send_header("Content-type", "application/pdf")
        self.send_header('Content-Disposition', 'attachment; filename="response.pdf"')

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        # Read the file and send the contents
        with open('response.pdf', 'rb') as file:
            self.wfile.write(file.read())

        return

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8080
my_server = socketserver.TCPServer(("", PORT), handler_object)

print("Http Server Serving at port", PORT)
# Star the server
my_server.serve_forever()
