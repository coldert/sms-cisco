from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse

PORT_NUMBER = 8080

class myRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    parsed_path = urlparse(self.path)
    query_array = parsed_path.query.split('&')
	#Call command parser
	#SSH to router
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    self.wfile.write(query_array)
    return
try:
  server = HTTPServer(('', PORT_NUMBER), myRequestHandler)
  print 'Started httpserver on port ', PORT_NUMBER, '. Ctrl-C to stop.'
  server.serve_forever()
except KeyboardInterrupt:
  print 'Shutting down the web server...'
  server.socket.close()

