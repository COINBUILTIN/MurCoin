from hashlib import sha256
from tx_validator import validate_tx
from merkle import merkle_tree


class Block:
    def __init__(self, timestamp, previous_hash, transactions, nonce=0):
        self.timestamp = timestamp
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.merkle_root = merkle_tree(transactions)
        self.hash_block = self.get_hash_block()

    def get_hash_block(self):
        block = (str(self.timestamp) +
                 str(self.nonce) +
                 str(self.previous_hash) +
                 "".join(self.transactions) +
                 self.merkle_root).encode("utf-8")
        hash_block = sha256(block).hexdigest()
        return hash_block

    def validate_transactions(self):
        if self.transactions:
            for tx in self.transactions:
                if validate_tx(tx) is False:
                    return False
            return True
