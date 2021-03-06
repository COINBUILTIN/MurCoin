from hashlib import sha256
from modules.transaction.tx_validator import validate_tx
from modules.block.merkle import merkle_tree


class Block:
    def __init__(self, timestamp, previous_hash, transactions, nonce=0):
        self.timestamp = timestamp
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.merkle_root = merkle_tree(transactions)
        self.hash = self.get_hash_block()

    # def get_hash_block(self):
    #     block = (str(self.timestamp) +
    #              str(self.nonce) +
    #              str(self.previous_hash) +
    #              "".join(self.transactions) +
    #              self.merkle_root)
    #     hash_block = sha256(block.encode("utf-8")).hexdigest()
    #     return hash_block

    def get_hash_block(self):
        block = (str(self.timestamp) +
                 str(self.nonce) +
                 str(self.previous_hash) +
                 str(self.transactions) +
                 self.merkle_root)
        hash_block = sha256(block.encode("utf-8")).hexdigest()
        return hash_block

    def validate_all_transactions(self):
        if self.transactions:
            for tx in self.transactions:
                if validate_tx(tx) is False:
                    return False
            return True

    def fill_dict(self):
        return {
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
            "transaction": self.transactions,
            "merkle_root": self.merkle_root,
            "hash": self.hash
        }
