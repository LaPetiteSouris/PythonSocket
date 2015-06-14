__author__ = 'tung'
import socket
import random
import hashlib

from users import Users

'''
This class start a TCP server to verify incoming connection.
Any incoming request will be challenged with password, and if username and password is verified,
server will issue a SHA-256 encription key for any further data transaction activity
'''


class TCPServer:
    def __init__(self, host='127.0.0.1', port=8081, user_namelist=[]):
        self._host = host
        self._port = port
        # create debug username
        user1 = Users()
        user1.username = 'debug'
        user1.password = '123'
        user_namelist.append(user1)
        user2 = Users()
        user2.username = 'deb'
        user2.password = '123'
        user_namelist.append(user2)
        self._listuser = user_namelist

    # start server
    def startauth_handshake(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self._host, self._port))
            s.listen(2)
            while True:
                try:
                    connection, addr = s.accept()
                    username = connection.recv(255)
                    print ('Received request from address: ', addr)
                    if username:
                        # Check if username exists

                        r = self.userchecking(username)
                        if r != -1:
                            print ('Server challenging for password...')
                            connection.sendall(str(r))
                            # H1 key received from client
                            h1 = connection.recv(255)
                            # Calculate H2
                            h2 = str(self._p1) + str(r)
                            h2hash = self.hashcalculator(h2)
                            # Auth success if H2 key calculated is equal to H1 key from client.
                            if h2hash == h1:
                                connection.sendall('Done')
                                print('Client answer accepted. Authentication completed')
                                break
                            # Auth fails if H2 key calculated is different with H1 key from client
                            elif h2hash != h1:
                                connection.sendall('Failed')
                                print('Client answer not accpeted. Authentication failed')
                                h2hash=None
                                break
                        elif r == -1:
                            print('User does not exist !')
                            connection.sendall('Failed')
                            h2hash=None
                            break
                finally:
                    connection.close()

        finally:
            print ('TCP Authentication Socket is closing')
            s.close()
        return h2hash

    def userchecking(self, username):
        for user in self._listuser:
            r = 0
            if user.username == username:
                # User exists. Return P1 password
                self._p1 = user.password
                # Now create a random number
                r = random.random()
                break
            else:
                user = None
                r = -1
        return r

    def hashcalculator(self, number):
        return hashlib.sha256(number).hexdigest()
