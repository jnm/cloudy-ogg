# jnm 20140820
import sys
import http.server
import cgi
import subprocess

port = None
try:
    port = int(sys.argv[1])
except (ValueError, IndexError):
    print('Usage:', sys.argv[0], 'PORT', file=sys.stderr)
    exit(1)

class OggifyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(400)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(
            "You don't really know what you're doing, do you?".encode('utf-8')
        )
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type']
            }
        )
        if 'file' not in form or not hasattr(form['file'], 'file'):
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(
                "I was expecting a bit more.".encode('utf-8')
            )
            exit(1)
        self.send_response(200)
        self.send_header('Content-Type', 'audio/ogg')
        self.send_header('Content-Disposition', 'attachment')
        self.end_headers()
        subprocess.call(
            ('ffmpeg', '-i', '-', '-vn', '-codec:a', 'libvorbis', '-f', 'ogg', '-'),
            stdin=form['file'].file,
            stdout=self.wfile
        )
server_address = ('', port)
httpd = http.server.HTTPServer(server_address, OggifyHandler)
httpd.serve_forever()
