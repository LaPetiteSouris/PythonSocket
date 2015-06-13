__author__ = 'tung'
import socket
import hmac
from hashlib import sha256
import pickle


class UDPServer:
    def __init__(self, host='127.0.0.1', port=8081, key='0'):
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._key = key

    def startTransmission(self, key):
        self._key = key
        s = self._sock
        s.bind((self._host, self._port))
        try:
            while True:
                data, addr = s.recvfrom(255)
                print('Received message from client address: ', addr, 'Verifying...')
                recvHMAC, pickled_data = data.split('  ')
                hmac_calculated = self.make_hmac(self._key, pickled_data)
                if self.compare_hmac(hmac_calculated, recvHMAC):
                    print('Message comes from verified client. Accepted. Echo back. Connection loop completed')
                    header = '%s' % (hmac_calculated)
                    s.sendto(header + '  ' + pickled_data, addr)
                    break
                else:
                    print('Unverified client attempt to connect. Shutdown socket now !')
                    break
        finally:
            s.close()

    def verifier(self, data, key, recvHMAC):
        return self.compare_hmac(recvHMAC, hash)

    # HMAC Make:
    def make_hmac(self, key, message):
        return hmac.new(key, message, sha256).hexdigest()

    # HMAC compare
    def compare_hmac(self, hmac1, hmac2):
        return self.compare_digest(hmac1, hmac2)

    def compare_digest(self, x, y):
        if not (isinstance(x, bytes) and isinstance(y, bytes)):
            raise TypeError("both inputs should be instances of bytes")
        if len(x) != len(y):
            return False
        result = 0
        for a, b in zip(x, y):
            result |= ord(a) ^ ord(b)
        return result == 0
