__author__ = 'tung'
import struct
import sys


class UDPProtocol:
    def __init__(self):
        # structure of the UDP data pakcage. Refer to http://www.cs.tut.fi/~hajap/assignments/socket/protocol/ for details
        s = struct.Struct('s s s !I !I !I s !I I')
        self._s = s

    def pack(self, message):
        packed_data = self._s.pack(*message)
        return packed_data

    def unpack(self, message):
        unpacked_data = self._s.unpack(message)
        return unpacked_data

    def dataverify(self, data):
        unpacked = self.unpack(data)
        if sys.getsizeof(unpacked[0]) != 1 | sys.getsizeof(unpacked[1]) != 1 | sys.getsizeof(
                unpacked[2]) != 2 | sys.getsizeof(unpacked[3]) != 4 | sys.getsizeof(unpacked[4]) != 4 | sys.getsizeof(
                unpacked[5]) != 2 | sys.getsizeof(unpacked[7]) != 2:
            return False
        else:
            return True
