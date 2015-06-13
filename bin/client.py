import hashlib
import socket
import hmac
from hashlib import sha256
import pickle


def verifier(buff, key):
    # Unpack received'!'+ at
    unpacked = packer.unpack(buff)
    hash = make_hmac(key, unpacked[1])
    return compare_hmac(unpacked[0], hash)

    # HMAC Make:


def make_hmac(key, message):
    return hmac.new(key, message, sha256).hexdigest()

# HMAC compare


def compare_hmac(hmac1, hmac2):
    return compare_digest(hmac1, hmac2)

def compare_digest(x, y):
    if not (isinstance(x, bytes) and isinstance(y, bytes)):
        raise TypeError("both inputs should be instances of bytes")
    if len(x) != len(y):
        return False
    result = 0
    for a, b in zip(x, y):
        result |= ord(a) ^ ord(b)
    return result == 0
print('Please enter your username')
u1 = raw_input()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8081))
s.sendall(u1)
r = s.recv(256)
if r != 'Failed':
    print('Please enter your password:')
    p1 = raw_input()
    h1 = str(p1) + str(r)
    h1hash = hashlib.sha256(h1).hexdigest()
    s.sendall(h1hash)
    result = s.recv(256)
    if result == 'Done':
        print('You are authorized to access ! Sending ping to server...')
        s.close()
        udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message='Ping'
        pickled_data=pickle.dumps(message)
        hmac_result=make_hmac(h1hash, pickled_data)
        header='%s' %(hmac_result)
        udpsock.sendto(header+'  '+pickled_data, ('127.0.0.1', 8081))
        echo=udpsock.recv(255)
        recvHMAC, pickled_data=echo.split('  ')
        hmac_calculated = make_hmac(h1hash, pickled_data)
        if compare_hmac(hmac_calculated, recvHMAC):
            print('Response comes from verified server. Accepted')
            print('Server response is ', pickle.loads(pickled_data))
            udpsock.close()
        else:
            udpsock.close()

    elif result == 'Failed':
        print('Authentication error')
        s.close()

elif r == 'Failed':
    print('Authentication error')
    s.close()




