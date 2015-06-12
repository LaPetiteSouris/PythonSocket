__author__ = 'tung'
import socket
import random
import hashlib

from bin.server.users import Users


class TCPServer:
    def __init__(self, host='127.0.0.1', port=8080, user_namelist=[]):
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    # start server, listening to username input
    def startauth_handshake(self):
        s = self._sock
        s.bind((self._host, self._port))
        s.listen(2)
        while True:
            connection, addr = s.accept()
            username = connection.recv(255)
            print ('Received data from address: ', addr)
            if username:
                # Check if username exists
                r = self.userchecking(username)
                if r != -1:
                    print ('Server responding')
                    connection.sendall(str(r))
                    # H1
                    h1 = connection.recv(255)
                    # Calculate H2
                    h2 = str(self._p1) + str(r)
                    h2hash = self.hashcalculator(h2)
                    # Auth success
                    if h2hash == h1:
                        connection.sendall('Done')
                        print('Connection accepted. Auth completed')
                        connection.close()
                        break
                    # Auth fails
                    elif h2hash != h1:
                        connection.sendall('Failed')
                        connection.close()
                        print('Connection closed. Auth failed')
                elif r == -1:
                    print('User does not exist !')
                    connection.sendall('Failed')
                    connection.close()
        return True

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
