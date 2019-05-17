import pyaes
from base64 import b64encode, b64decode
import config
import json

# b64key is 32 bytes encoded in base64
# data is byte encoded string
class AESData:
    def __init__(self, b64key, data):
        self.b64key = b64key
        self.data = data

    def encrypt(self):
        key = b64decode(self.b64key)
        aes = pyaes.AESModeOfOperationCTR(key)
        ciphertext = aes.encrypt(json.dumps(self.data))
        return {
            "cipher": b64encode(ciphertext).decode("utf-8")
        }

# b64key is 32 bytes encoded in base64
# b64cipher is b64 encoded cipher bytes
class AESCipher:
    def __init__(self, b64key, b64cipher):
        self.b64key = b64key
        self.b64cipher = b64cipher
    def decrypt(self):
        cipher = b64decode(self.b64cipher)
        key = b64decode(self.b64key)
        aes = pyaes.AESModeOfOperationCTR(key)
        data = aes.decrypt(cipher)
        return {
            "data": data
        }

# used for decorator function 
class encrypt(object):
    def __init__(self, f):
        self.f = f

    def __call__(self):
        data = self.f(self)
        aesdata = AESData(config.B64KEY, data)
        return aesdata.encrypt()