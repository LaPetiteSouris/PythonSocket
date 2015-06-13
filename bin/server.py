__author__ = 'tung'

from bin.server import TCPServer
from bin.server import UDPServer
server=TCPServer()
hashkey=server.startauth_handshake()
if hashkey:
    print ('Hand shake completed. Data transmission initiated...')
    #TO-DO: Start UDP transmission here
    udpserver =UDPServer()
    udpserver.startTransmission(hashkey)


