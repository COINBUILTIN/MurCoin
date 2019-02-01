import ecdsa
import hashlib
from base58 import b58decode
from ecdsa import SigningKey, SECP256k1
from hashlib import sha256
from binascii import unhexlify, hexlify
from utilitybelt import dev_random_entropy


def double_sha256(key):
    return sha256(sha256(unhexlify(key)).digest()).hexdigest()


a = [1, 2, 3, 4]
a.append(a[-1])
for i in a:
    print(i)