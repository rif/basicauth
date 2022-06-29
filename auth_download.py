import http.server
import cgi
import base64
import json
from urllib.parse import urlparse, parse_qs


class CustomServerHandler(http.server.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm="Demo Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()
        print("HEADERS: ", self.headers)

        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + str(key):
              self.send_response(200)

              # Setting the headers
              self.send_header("Content-type", "application/pdf")
              self.send_header('Content-Disposition', 'attachment; filename="response.pdf"')

              # Whenever using 'send_header', you also have to call 'end_headers'
              self.end_headers()

              # Read the file and send the contents
              with open('response.pdf', 'rb') as file:
                  self.wfile.write(file.read())
        else:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))



class CustomHTTPServer(http.server.HTTPServer):
    key = ''

    def __init__(self, address, handlerClass=CustomServerHandler):
        super().__init__(address, handlerClass)

    def set_auth(self, username, password):
        self.key = base64.b64encode(
            bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


if __name__ == '__main__':
    server = CustomHTTPServer(('', 8000))
    server.set_auth('adi', 'test')
    server.serve_forever()
