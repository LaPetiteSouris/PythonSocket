__author__ = 'tung'

from server import TCPServer

server=TCPServer()
if server.startauth_handshake():
    print 'Hand shake completed. Initiated communication...'
    #TO-DO: Start UDP transmission here


