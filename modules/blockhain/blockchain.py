from modules.server import *
from modules.block import Block


class Blockchain:
    def __init__(self):
        self.difficulty = 2
        self.chain = []
        self.url = "http://" + HOST + ":" + PORT


    # def mine(self, block=None):
    #     if not block:
    #         block = self.create_block_with_tx()
    #     while block
    #
    #
    # def create_block_with_tx(self):
    #     pass
