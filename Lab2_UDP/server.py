import socket
from generator import generate
from datetime import datetime

from client import NO_OFF_T
from client import PACK_SIZE
from client import PACKS_COUNT

TIMEOUT = 5.0
EFFORTS_COUNT = 100


class Server:
    def __init__(self, port):
        self.sock = None
        self.port = port

        self.total_time = None
        self.received = 0
        self.buffer = []
        self.received = {}
        self.total_received = 0

        self.clientInfo = None

    def measure(self):
        self.sock.settimeout(None)

        self.total_time = 0
        self.buffer.clear()

        print("Waiting...")

        req, self.clientInfo = self.sock.recvfrom(PACK_SIZE)
        self.buffer.append(req)

        start_time = last_time = datetime.now()

        self.sock.settimeout(TIMEOUT)

        try:
            while 1:
                req = self.sock.recv(PACK_SIZE)
                self.buffer.append(req)
                last_time = datetime.now()

        except socket.timeout:
            print("------------------")

        self.total_time = last_time - start_time

    def analyze(self):
        self.total_received = 0

        for pack in self.buffer:
            pack_no = int.from_bytes(pack[:NO_OFF_T], byteorder='little')
            pack_data = int.from_bytes(pack[NO_OFF_T:], byteorder='little')

            if pack_data == generate(pack_no):
                self.total_received += 1
                res = '+'
            else:
                res = '-'

            print("{}: {} ({})".format(pack_no, pack_data, res))

    def send_result(self):
        self.total_time = self.total_time.seconds * 10**6 + self.total_time.microseconds
        self.total_time = 1 if self.total_time == 0 else self.total_time

        result = "Packets received:\t{}/{}\n".format(self.total_received, PACKS_COUNT)
        result += "Packets lost:\t{}\n".format(PACKS_COUNT - self.total_received)

        full_size = PACK_SIZE * self.total_received
        result += "Overall size:\t{} bytes\n".format(full_size)
        result += "Overall time:\t{} mcsec\n".format(self.total_time)

        speed = ((full_size // 1024) / self.total_time) * 10**6  # in KB/sec
        result += "Speed:\t~{0:.2f} KB/sec\n".format(speed)

        print(result)
        print("\n<=========================\n")

        print(self.clientInfo[0])

        result = bytearray(result.ljust(PACK_SIZE), encoding='utf-8')
        for i in range(EFFORTS_COUNT):
            self.sock.sendto(result, self.clientInfo)

    def start(self):
        print("Server started")

        try:
            while 1:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind(("", self.port))

                try:
                    self.measure()
                    self.analyze()
                    self.send_result()

                finally:
                    self.sock.close()

        except (KeyboardInterrupt, SystemExit):
            print("Closed by user")
