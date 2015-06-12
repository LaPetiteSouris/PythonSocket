__author__ = 'tung'
import socket
import hmac
from hashlib import sha256
class UDPServer:
    def __init__(self,host='127.0.0.1', port=8080):
        self._host =host
        self._port =port
        self._sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def startTransmission(self, message=''):
        s=self._sock
        s.bind(self._host, self._port)
        while True:
            addr, data=s.recvfrom(255)
            print ('Received message from client address: ', addr)



