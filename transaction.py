import wallet
from hashlib import sha256


class Transaction:
    def __init__(self, sender=None, recipient=None, amount=None):
        if not sender:
            raise ValueError("Sender address is missing")
        if not recipient:
            raise ValueError("Recepient address is missing")
        if not amount:
            raise ValueError("Amount is missing")
        if amount <= 0:
            raise ValueError("Amount must be bigger than zero")

        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def get_hash(self):
        tx = self.sender + self.recipient + str(self.amount)
        tx_hash = sha256(tx.encode("utf-8")).hexdigist()
        return tx_hash

    def get_signature(self, signature, ext_pub_key):
        self.signature = signature.hex()
        self.verify_pub_key = ext_pub_key[2:]


class CoinbaseTransaction(Transaction):
    def __init__(self):
        self.private_key = wallet.wif_to_private_key("minerkey")
        recipient = open("address", "r").readline()
        super().__init__(34*"0", recipient, 50)
