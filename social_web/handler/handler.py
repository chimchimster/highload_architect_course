from pathlib import Path


from http.server import BaseHTTPRequestHandler
from social_web.jinja_handler import render_template


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

                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()

                    rendered_html = render_template('index.html', {'header': 'Hello, world!'})

                    self.wfile.write(rendered_html.encode())

                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()

                    not_found = Path(self.base_templates_directory) / 'not_found.html'
                    print(type(not_found))
                    rendered_html = render_template(str(not_found))

                    self.wfile.write(rendered_html.encode())
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                not_found = Path(self.base_templates_directory) / 'not_found.html'

                rendered_html = render_template(str(not_found))
                self.wfile.write(rendered_html)
        except Exception as e:

            self.send_response(500)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f'Internal Server Error: {str(e)}'.encode())
