import socket

class MySock:


    def __init__(self, socK = None):
        if socK:
            self.socket = socK
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self, host, port):
        self.socket.connect((host, port))

    def settimeout(self, timeout=0):
        self.socket.settimeout(timeout)

    def bind(self, host, port):
        self.socket.bind((host, port))

    def listen(self, backlog=None):
        self.socket.listen(backlog)

    def accept(self):
        return self.socket.accept()

    def send(self, msg, size):
        total_sent = 0
        while total_sent < size:
            sent = self.socket.send(msg[total_sent:])
            if sent == 0:
                raise ConnectionAbortedError("Socket connection broken")

            total_sent = total_sent + sent

    def recv(self, size):
        chunks = bytearray(size)
        bytes_recd = 0

        while bytes_recd < size:
            chunk = self.socket.recv(min(size - bytes_recd, 2048))
            if chunk == '':
                raise ConnectionAbortedError("Socket connection broken")

            chunks[bytes_recd:] = chunk
            bytes_recd += len(chunk)

        return chunks

    def close(self):
        self.socket.close()                                     
