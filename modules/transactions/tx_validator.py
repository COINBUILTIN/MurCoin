import wallet
from hashlib import sha256
from ecdsa import VerifyingKey, SECP256k1
from .serializer import Deserializer
from .transaction import Transaction


def check_address(address):
    if address[0] is not '1':
        return False
    valid_checksum = wallet.validate_checksum(address)
    if valid_checksum is False:
        return False
    return True


def compare_public_key_with_address(address, public_key):
    valid_address = wallet.public_key_to_address(public_key, 0)
    if valid_address == address:
        return True
    return False


def check_signature(signature, public_key, hash_m):
    verify_key = VerifyingKey.from_string(bytes.fromhex(public_key[2:]), curve=SECP256k1, hashfunc=sha256)
    return verify_key.verify(signature, hash_m.encode("utf-8"))


def validate_tx(trans, hash_tx):
    tx = Deserializer(trans).get_params()
    print(tx['sender'])
    print(tx['recipient'])
    print(tx['amount'])
    curr_tx = Transaction(tx['sender'], tx['recipient'], tx['amount'])
    if check_address(tx['sender']) is False:
        print("Error: sender is invalid")
        return False
    if check_address(tx['recipient']) is False:
        print("Error: recipient is invalid")
        return False
    if compare_public_key_with_address(tx['sender'], tx['verify_pub_key']) is False:
        print("Error: public key doesn't belong to the sender")
        return False
    if not check_signature(tx['signature'], tx['verify_pub_key'], hash_tx):
        print("Error: signature is invalid")
        return False
    return True
