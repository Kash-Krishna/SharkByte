
import SocketServer

class MyTCPSocketHandler(SocketServer.BaseRequestHandler) :
    """
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self) :

        self.data = self.request.recv(1024).strip()
        print("{} wrote".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.data.upper())

if __name__ == "__main__" :
    HOST, PORT = "localhost", 5000

    server = SocketServer.TCPServer((HOST, PORT), MyTCPSocketHandler)
    server.serve_forever()
    
    
