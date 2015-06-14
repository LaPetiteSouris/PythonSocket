__author__ = 'tung'

from server import TCPServer
from server import UDPServer
server=TCPServer()
hashkey=server.startauth_handshake()
if hashkey is not None:
    print ('Hand shake completed. Data transmission initiated via UDP Protocol...')
    #Start UDP transmission if user is verified
    udpserver =UDPServer()
    udpserver.startTransmission(hashkey)


