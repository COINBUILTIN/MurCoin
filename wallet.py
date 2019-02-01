import ecdsa
import hashlib
from base58 import b58decode
from ecdsa import SigningKey, SECP256k1
from hashlib import sha256
from binascii import unhexlify, hexlify
from utilitybelt import dev_random_entropy


# Constants


p = 2 ** 256 - 2 ** 32 - 977
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
g = (Gx, Gy)


# Tools


def check_point_on_curve(pt, p):
    (x, y) = pt
    if (x ** 3 + 7 - y ** 2) % p == 0:
        return True
    return False


def validate_coordinates(pub_key):
    cords = pub_key
    hex_x = cords[:64]
    hex_y = cords[64:]
    x = int(hex_x, 16)
    y = int(hex_y, 16)
    pt = (x, y)
    if check_point_on_curve(pt, p):
        return True
    return False


def double_sha256(key):
    return sha256(sha256(unhexlify(key)).digest()).hexdigest()


def validate_checksum(string):
    hex_string = b58decode(string).hex()
    last_bytes = hex_string[-8:]
    tmp_string = hex_string[:-8]
    new_string = double_sha256(tmp_string)
    first_bytes = new_string[:8]
    print("last -> " + last_bytes)
    print("last -> " + first_bytes)
    if first_bytes == last_bytes:
        return True
    return False


def base58(address_hex):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    b58_string = ""
    leading_zeros = len(address_hex) - len(address_hex.lstrip("0"))
    address_int = int(address_hex, 16)
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    ones = leading_zeros // 2
    for one in range(ones):
        b58_string = "1" + b58_string
    return b58_string


def create_signature(private_key, hash_massage):
    hash_massage = hash_massage.encode("utf-8")
    private_key_bytes = unhexlify(private_key)
    sign_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    verify_key = sign_key.get_verifying_key()
    signature = sign_key.sign(hash_massage)
    assert verify_key.verify(signature, hash_massage)
    return signature, verify_key.to_string().hex()


def public_key_to_address(public_key, testnet):
    sha256_pub_key = sha256(unhexlify(public_key)).digest()
    ripemd160_pub_key = hashlib.new('ripemd160')
    ripemd160_pub_key.update(sha256_pub_key)
    ripemd160_pub_key_digest = ripemd160_pub_key.digest()
    ripemd160_pub_key_hex = hexlify(ripemd160_pub_key_digest)
    if testnet:
        network_pub_key = b'6f' + ripemd160_pub_key_hex
    else:
        network_pub_key = b'00' + ripemd160_pub_key_hex
    checksum = double_sha256(network_pub_key)[:8].encode("utf-8")
    hex_address = (network_pub_key + checksum).decode("utf-8")
    wallet_address = base58(hex_address)
    return wallet_address


def wif_to_private_key(path_to_wif_key):
    wif = open(path_to_wif_key, "r").readline()
    hex_wif = b58decode(wif).hex()
    compressed = 1 if hex_wif[67] == '1' else 0
    hex_wif = hex_wif[:-10] if compressed else hex_wif[:-8]
    priv_key = hex_wif[2:]
    return priv_key


def private_key_to_wif(private_key, testnet, compressed):
    if testnet:
        private_key = "ef" + private_key
    else:
        private_key = "80" + private_key
    if compressed:
        private_key = private_key + "01"

    checksum = double_sha256(private_key)[:8]
    final_key = private_key + checksum
    wif_key = base58(final_key)
    return wif_key


def get_compressed_public_key(private_key, save_to_file):
    file = open("compr_pub_key", "w")
    private_key_bytes = unhexlify(private_key)
    verify_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1).get_verifying_key()
    hex_key = verify_key.to_string().hex()
    half_key = hex_key[:64]
    last_byte = int(hex_key[-1], 16)
    y_byte = "02" if last_byte % 2 == 0 else "03"
    public_key = y_byte + half_key
    if save_to_file:
        file.write(public_key)
    return public_key


def get_ext_public_key(private_key, save_to_file):
    file = open("ext_pub_key", "w")
    private_key_bytes = unhexlify(private_key)
    verify_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1).get_verifying_key()
    hex_key = verify_key.to_string().hex()
    public_key = "04" + hex_key
    if save_to_file:
        file.write(public_key)
    return public_key


def random_exponent(curve):
    while 1:
        random_hex = hexlify(dev_random_entropy(32))
        random_int = int(random_hex, 16)
        if 1 <= random_int < curve:
            return random_int


def get_private_key():
    curve = ecdsa.curves.SECP256k1
    rp = random_exponent(curve.order)
    key = SigningKey.from_secret_exponent(rp, curve, sha256)
    hex_key = key.to_string().hex()
    return hex_key
