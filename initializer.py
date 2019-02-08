import os
import errno
import requests

from modules.server import *
from modules.blockchain import Blockhain


def check_path(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

    try:
        os.remove(path + "blocks.txt")
        os.remove(path + "mempool.txt")
        os.remove(path + "utxopool.txt")
    except OSError:
        pass


def create_genesis_block():
    blockchain = Blockchain()
    genesis_block = blockchain.genesis_block()
    url = "http://" + HOST + ":" + PORT
    requests.post(url + "/chain/block" + str(genesis_block))


check_path("modules/storage/")
create_genesis_block()
