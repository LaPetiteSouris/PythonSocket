__author__ = 'tung'
import hmac
from hashlib import sha256


class HMACVerifier:
    def make_hmac(self, key, message):

        return hmac.new(key, message, sha256).hexdigest()

    # hmac_package compare
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
