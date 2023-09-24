import logging
from http.server import BaseHTTPRequestHandler
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)


class RequestHandler(BaseHTTPRequestHandler):

    base_templates_directory = './templates'

    routes = {
        '/': 'index.html',

    }

    def do_GET(self):
        try:

            if self.path in self.routes:
                file_name = self.routes[self.path]
                file_path = Path(self.base_templates_directory) / file_name

                if file_path.is_file():

                    with open(file_path, 'rb') as file:
                        content = file.read()

                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()

                    not_found = Path(self.base_templates_directory) / 'not_found.html'

                    with open(not_found, 'rb') as file:
                        content = file.read()

                    self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                not_found = Path(self.base_templates_directory) / 'not_found.html'

                with open(not_found, 'rb') as file:
                    content = file.read()

                self.wfile.write(content)
        except Exception as e:

            self.send_response(500)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f'Internal Server Error: {str(e)}'.encode())
