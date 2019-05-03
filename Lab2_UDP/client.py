import socket
from generator import generate

NO_OFF_T = 8
PACK_SIZE = 4096
PACKS_COUNT = 100

TIMEOUT = 10.0

class Client:
    def __init__(self, srv_address, port, packets_count=PACKS_COUNT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.srv_address = srv_address
        self.srv_port = port

        self.packets_count = packets_count

    def form_packet(self, pack_no, data):
        result = bytearray(PACK_SIZE)
        result[:NO_OFF_T] = int.to_bytes(pack_no, NO_OFF_T, byteorder='little')
        result[NO_OFF_T:] = int.to_bytes(data, PACK_SIZE - NO_OFF_T, byteorder='little')

        return result

    def measure(self):
        for i in range(self.packets_count):
            pack = generate(i+1)

            request = self.form_packet(i+1, pack)
            self.sock.sendto(request, (self.srv_address, self.srv_port))

    def get_result(self):
        self.sock.settimeout(TIMEOUT)
        try:
            result = self.sock.recv(PACK_SIZE)

        except socket.timeout:
            return "No answer"

        return result.decode('utf-8').strip()

    def start(self):
        print("Client started")

        try:
            self.measure()
            result = self.get_result()

        finally:
            self.sock.close()

        print(result)
