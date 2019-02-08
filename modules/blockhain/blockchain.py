import json
from time import gmtime, strftime

from modules.server import *
from modules.colors import *
from modules.transaction import *
from modules.block import Block


class Blockchain:
    def __init__(self):
        self.difficulty = 2
        self.chain = []
        self.url = "http://" + HOST + ":" + PORT

    def mine(self, block):
        while block.hash[0:self.difficulty] != '0' * self.difficulty:
            block.nonce += 1
            block.hash = block.get_hash_block()
            if block.nonce % 100 == 0:
                time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                pr_cyan('[' + time_str + '] nonce=' + str(block.nonce) + ', hash=' + block.hash)

        time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        pr_green('[' + time_str + '] nonce=' + str(block.nonce) + ', hash=' + block.hash)
        self.chain.append(block)
        height = len(self.chain) - 1

        block_file = open(ROOT + "/block." + ("%08i" % height), 'w+')
        json.dump(block.fill_dict(), block_file)
        block_file.close()

        block_height = open(ROOT + "/block_height", 'w')
        block_height.write(str(height + 1))
        block_height.close()

        return block

    def genesis_block(self):
        tx = CoinbaseTransaction()
        real_time = str(int(time.time()))
        serialize_tx =
        genesis = Block(real_time, '0' * 64, serialize_tx)

    # def check_hash(self, h):
    #     if h[0:self.difficulty] == '0' * self.difficulty:
    #         return True
    #     return False

