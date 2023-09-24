import http.server
import socketserver


def main():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    main()