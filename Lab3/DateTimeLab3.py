from socket import *
import struct
import sys
import time

NTP_SERVER = "pool.ntp.org"
TIME1970 = 2208988800

clientSocket = socket(AF_INET, SOCK_DGRAM)

portNumber = 123

def sntp_client():

    data = '\x1b' + 47 * '\0'

    clientSocket.sendto( data.encode('utf-8'), ( NTP_SERVER, portNumber ))

    data, address = clientSocket.recvfrom(1024)

    if data:
        print ('Response received from:', address)

        t_time = struct.unpack( '!12I', data )[10]

        t_time -= TIME1970

        print ('Time= ',time.ctime(t_time))

    clientSocket.close()
#main
if __name__ == '__main__':
    
    sntp_client()
