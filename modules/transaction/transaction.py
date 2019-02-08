from hashlib import sha256

from modules.wallet import *


class Transaction:
    signature: object
    verify_pub_key: object

    def __init__(self, sender=None, recipient=None, amount=None):
        if not sender:
            raise ValueError("Error: sender address is missing")
        if not recipient:
            raise ValueError("Error: recipient address is missing")
        if not amount:
            raise ValueError("Error: amount is missing")
        # if amount <= 0:
        #     raise ValueError("Error: amount must be bigger than zero")

        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def get_hash(self):
        tx = self.sender + self.recipient + str(self.amount)
        tx_hash = sha256(tx.encode("utf-8")).hexdigest()
        return tx_hash

    def get_signature(self, signature, ext_pub_key):
        self.signature = signature
        self.verify_pub_key = ext_pub_key


class CoinbaseTransaction(Transaction):
    def __init__(self):
        self.private_key = wallet.wif_to_private_key("minerkey")
        recipient = open("data/address", "r").readline()
        super().__init__(34*"0", recipient, 50)
