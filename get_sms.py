from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
from urllib import unquote
import sms_tolk2 as SMS

PORT_NUMBER = 8080

class ReceivedSmsHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		command = ""
		parsed_path = urlparse(self.path)
		query_list = parsed_path.query.split('&')
		for i in query_list:
			part = i.split('=')
			if part[0] == 'text': command = unquote(part[1])
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(SMS.parse(command))
		return
try:
	server = HTTPServer(('', PORT_NUMBER), ReceivedSmsHandler)
	print 'Started httpserver on port ', PORT_NUMBER, '. Ctrl-C to stop.'
	server.serve_forever()
except KeyboardInterrupt:
	print 'Shutting down the web server...'
	server.socket.close()

