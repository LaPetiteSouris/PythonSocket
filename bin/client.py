import socket
import pickle
import hashlib
from hmac_security import HMAC

'''
This is a simulated client. Client work flow is as below:
1.Ask username, send username to server for verification,
2.If user exists, received a authenticated string key from server . Then, challenge for password, else, termincate process
3.Ask for password. Use authenticated string to encripted password data. Send encripted data to server.
4.If authentication completes, client will receive a hash key. This hash key is used to calculate HMAC value. Every future communication
with server must include a HMAC key as header.
Else, termincate connection.
'''
# Create first a verifier package to verify HMAC key
verifier = HMAC.HMACVerifier()
# Ask username input
print('Please enter your username')
u1 = raw_input()
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8081))
    s.sendall(u1)
    r = s.recv(256)
    # If user name exist:
    if r != 'Failed':
        print('Please enter your password:')
        p1 = raw_input()
        h1 = str(p1) + str(r)
        # Calculate hash value, send this value to server for verification. If correct
        # this will be hashkey to calculate HMAC verification
        h1hash = hashlib.sha256(h1).hexdigest()
        s.sendall(h1hash)
        result = s.recv(256)
        if result == 'Done':
            print('You are authorized to access ! Sending ping to server...')
            # Start an UDP socket for data transation
            try:
                udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                message = 'Ping'
                pickled_data = pickle.dumps(message)
                # Add HMAC as header for ping transaction
                hmac_result = verifier.make_hmac(h1hash, pickled_data)
                header = '%s' % (hmac_result)
                udpsock.sendto(header + '  ' + pickled_data, ('127.0.0.1', 8081))
                # Received data from server, then verifiy with HMAC
                echo = udpsock.recv(255)
                recvHMAC, pickled_data = echo.split('  ')
                hmac_calculated = verifier.make_hmac(h1hash, pickled_data)
                if verifier.compare_hmac(hmac_calculated, recvHMAC):
                    print('Response comes from verified server. Accepted.')
                    print('Server response is ', pickle.loads(pickled_data))

                else:
                    print('Response comes from unverified server. Rejected.')
            finally:
                udpsock.close()
        elif result == 'Failed':
            print('Authentication error')  # If username does not exist
    elif r == 'Failed':
        print('Authentication error')
finally:
    s.close()
