__author__ = 'tung'
import socket
from hmac_security import HMAC

'''
This class handles the main information exchange between client and server.
Every transaction must attached with it a header, consist of the common hmac_package key, encripted
SHA-256 to verify integrity of the data. Any data which fails to comply will be rejected, socket
will be shutdown to avoid any further inflitration.
'''


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
        # Create a hmac_package verifier object
        verifier = HMAC.HMACVerifier()
        try:
            while True:
                data, addr = s.recvfrom(255)
                print('Received message from client address: ', addr, 'Verifying...')
                recvHMAC, pickled_data = data.split('  ')
                hmac_calculated = verifier.make_hmac(self._key, pickled_data)
                if verifier.compare_hmac(hmac_calculated, recvHMAC):
                    print('Message comes from verified client. Accepted. Echo back. Connection loop completed')
                    header = '%s' % (hmac_calculated)
                    s.sendto(header + '  ' + pickled_data, addr)
                    break
                else:
                    print('Unverified client attempt to connect. Shutdown socket now !')
                    break
        finally:
            s.close()
