import socketserver
import sys
import console


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        self.request.sendall(data.upper())


if __name__ == "__main__":
    host = console.host_params(sys.argv)
    server = socketserver.TCPServer(host, TCPHandler)
    server.serve_forever()
