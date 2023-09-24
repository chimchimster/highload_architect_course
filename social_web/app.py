import socket
import socketserver
from handler.handler import RequestHandler


def main():

    host, port = "127.0.0.1", 8000

    server_obj = socketserver.TCPServer((host, port), RequestHandler)
    server_obj.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    with server_obj as httpd:
        socketserver.TCPServer.allow_reuse_address = True
        httpd.serve_forever()


if __name__ == '__main__':
    main()