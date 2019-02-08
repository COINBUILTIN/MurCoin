import os
import cmd
import sys
import requests
import subprocess

from pyfiglet import Figlet

from modules.server import *
from modules.wallet import *
from modules.transaction.tx_validator import validate_tx
from modules.transaction.serializer import Serializer
from modules.transaction.transaction import Transaction

PRIVATE_KEY = []


def yes_or_no(rule):
    print(rule)
    while True:
        answer = input("Type (y/n): ")
        if answer == "y" or answer == "n":
            data = 1 if (answer == "y") else 0
            break
        else:
            print("Invalid input, try again.")
    return data


class MurCoin(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.tx_list = []
        self.prompt = "(💲Wallet-Client💲) → ️"

        f = Figlet(font='slant')
        s = f.renderText('M U R C O I N')

        self.intro = s + "\n         >>>> Welcome to the MurCoin wallet <<<<\n\n" \
                         "           Type 'help' or '?'  to list commands\n" \
                         "           Type 'exit' to safe exit from wallet\n\n"
        self.doc_header = "Possible commands (for reference of specific command type 'help [command]'"


    @staticmethod
    def do_exit(argv):
        """"Quit from wallet"""
        answer = yes_or_no("Do you want to delete data?")
        if answer:
            print("Clearing data...")
            if os.path.exists("data/pending_pool"):
                os.remove("data/pending_pool")
            if os.path.exists("data/cmpr_pub_key"):
                os.remove("data/cmpr_pub_key")
            if os.path.exists("data/ext_pub_key"):
                os.remove("data/ext_pub_key")
            if os.path.exists("data/wif_key"):
                os.remove("data/wif_key")
            if os.path.exists("data/minerkey"):
                os.remove("data/minerkey")
            if os.path.exists("data/address"):
                os.remove("data/address")
        sys.exit()

    @staticmethod
    def do_EOF(argv):
        return True

    @staticmethod
    def do_clear(argv):
        """"Clear screen"""
        subprocess.call("clear")

    @staticmethod
    def do_pwd(argv):
        """"Show path to current directory"""
        subprocess.call("pwd", shell=True)

    @staticmethod
    def do_ls(argv):
        """Show objects in current directory"""
        subprocess.call("ls")

    @staticmethod
    def do_show(argv):
        """Show your current private key"""

        global PRIVATE_KEY

        print("Private Key: '" + PRIVATE_KEY + "'")

    def do_send(self, argv):
        """Create transaction to send coins\nUsage: send [recipient address], [amount]"""

        global PRIVATE_KEY

        if not argv or len(argv.split(' ')) != 2:
            print("Usage: send [recipient address], [amount]")
            return

        split_argv = argv.split(' ')
        recipient = split_argv[0]
        amount = int(split_argv[1])
        try:
            file = open("data/address", 'r')
        except Exception as exc:
            print("You didn't get address, use command 'new' or 'import'")
            return
        sender = file.read()
        file.close()

        tx = Transaction(sender, recipient, amount)
        tx_hash = tx.get_hash()
        if not PRIVATE_KEY:
            print("You don't have private key, get one by command 'new'")
            return
        signature, ext_pub_key = wallet.create_signature(PRIVATE_KEY, tx_hash)
        print("SIGN", signature)
        tx.get_signature(signature, ext_pub_key)
        serialized_tx = Serializer(tx).get_serialize_tx()
        if validate_tx(serialized_tx, tx_hash) is False:
            return
        print('Send from [' + sender + '] to [' + recipient + '] amount -> [' + str(amount) + ']')
        print('Serialized transaction : [' + serialized_tx + ']')
        self.tx_list.append(serialized_tx)
        print("Transactions for broadcast: ")
        print(self.tx_list)

    def do_broadcast(self, argv):
        """Broadcasting transaction"""

        url = "http://" + str(server.ip) + ":" + str(server.port) + "/transaction/new"

        payload = {"transaction": []}
        try:
            pool = open("data/pending_pool", 'w')
            for tx in self.tx_list:
                pool.write(tx)
                payload["transaction"].append(tx)
            pool.close()

            header = {"Content-Type": "application/json"}
            req = requests.post(url, json=payload, headers=header)
            print("Transactions successfully broadcasted")

            file = open("data/transaction", 'w')
            file.write('')
            file.close()
        except Exception as exc:
            print(exc)
            print("Broadcast Error")

    @staticmethod
    def do_import(argv):
        """Import WIF key from file\nUsage: import ./path/file_name_with_wif_key"""

        global PRIVATE_KEY

        if os.path.exists(argv):
            PRIVATE_KEY = wallet.wif_to_private_key(argv)
            cmpr_pub_key = wallet.get_compressed_public_key(PRIVATE_KEY, 0)
            testnet = yes_or_no("Do you use testnet?")
            addr = wallet.public_key_to_address(cmpr_pub_key, testnet)
            print("Wallet address is: '" + addr + "'")
            open("data/address", "w").write(addr)
            print("Public address was saved to 'data/address'.")
        else:
            print("No such file or directory: '" + argv + "'")

    @staticmethod
    def do_minerkey(argv):
        """Create file with WIF key for mining"""

        global PRIVATE_KEY

        if not PRIVATE_KEY:
            print("Error: private key is missing. Use command 'new' to generate key")
        else:
            PRIVATE_KEY = wallet.get_private_key()
            minerkey = wallet.private_key_to_wif(PRIVATE_KEY, 0, 0)
            file = open("data/minerkey", "w")
            file.write(minerkey)
            print("Minerkey was created in WIF format and saved to 'data/minerkey'")
            file.close()

    @staticmethod
    def do_wif(argv):
        """Convert your private key to WIF format\n"""

        global PRIVATE_KEY

        if not PRIVATE_KEY:
            print("Error: private key is missing, use command 'new' to generate one")
        else:
            testnet = yes_or_no("Do you use testnet?")
            compressed = yes_or_no("Use compressed format for WIF?")
            wif = wallet.private_key_to_wif(PRIVATE_KEY, testnet, compressed)
            print("WIF format key: '" + wif + "'")
            # check = yes_or_no("Save WIF key to file calls 'wif_key'?")
            # if check:
            file = open("data/wif_key", "w")
            file.write(wif)
            file.close()

    @staticmethod
    def do_new(argv):
        """Get new key pair (private and public)\nSave public key to 'data/cmpr_pub_key'"""

        global PRIVATE_KEY

        if not PRIVATE_KEY:
            PRIVATE_KEY = wallet.get_private_key()
        else:
            get_new = yes_or_no("Private key already exist, do you want generate new one ?")
            if get_new:
                PRIVATE_KEY = wallet.get_private_key()
        print("Private Key: '" + PRIVATE_KEY + "'")
        cmpr_pub_key = wallet.get_compressed_public_key(PRIVATE_KEY, 1)
        addr = wallet.public_key_to_address(cmpr_pub_key, 0)
        open("data/address", "w").write(addr)
        print("Public key was saved to 'data/cmpr_pub_key'")


if __name__ == '__main__':
    MurCoin().cmdloop()
