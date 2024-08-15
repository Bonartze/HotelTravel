import socket

class ServerConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))

    def send_message(self, message):
        if self.socket:
            self.socket.sendall(message)
            data = self.socket.recv(1024)
            return data.decode('utf-8')
        else:
            raise ConnectionError("Socket is not connected.")

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
