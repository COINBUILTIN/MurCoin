import cmd
import os
import subprocess
import sys

from pyfiglet import Figlet

import wallet

PRIVATE_KEY = None
# MEMPOOL = []


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


class PitCoin(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "(💲Wallet-Client💲) → ️"

        f = Figlet(font='slant')
        s = f.renderText('M U R C O I N')

        self.intro = s + "\n         >>>> Welcome to the PitCoin wallet <<<<\n\n" \
                         "           Type 'help' or '?' to list commands\n" \
                         "           Type 'exit' to safe exit from wallet\n\n"
        self.doc_header = "Possible commands (for reference of specific command type 'help [command]'"


    @staticmethod
    def do_exit(arg):
        "Quit from wallet"
        answer = yes_or_no("Do you want to delete data key?")
        if answer:
            print("Clearing data...")
            if os.path.exists("compr_pub_key"):
                os.remove("compr_pub_key")
            if os.path.exists("ext_pub_key"):
                os.remove("ext_pub_key")
            if os.path.exists("wif_key"):
                os.remove("wif_key")
            if os.path.exists("minerkey"):
                os.remove("minerkey")
            if os.path.exists("address"):
                os.remove("address")
        sys.exit()

    @staticmethod
    def do_clear(arg):
        "Clear screen"
        subprocess.call("clear")

    @staticmethod
    def do_pwd(arg):
        "Show path to current directory"
        subprocess.call("pwd", shell=True)

    @staticmethod
    def do_ls(arg):
        "Show objects in current directory"
        subprocess.call("ls")

    @staticmethod
    def do_show(arg):
        "Show your current private key"
        global PRIVATE_KEY
        print("Private Key: '" + PRIVATE_KEY + "'")

    # @staticmethod
    # def do_send(arg, argv):
    #     ar = argv.split(argv)

    @staticmethod
    def do_import(arg):
        "Import WIF key from file.\nUsage: import ./path/file_name_with_wif_key"
        global PRIVATE_KEY
        if os.path.exists(arg):
            PRIVATE_KEY = wallet.wif_to_private_key(arg)
            compr_pub_key = wallet.get_compressed_public_key(PRIVATE_KEY, 0)
            testnet = yes_or_no("Do you use testnet?")
            addr = wallet.public_key_to_address(compr_pub_key, testnet)
            print("Wallet address is: '" + addr + "'")
            open("address", "w").write(addr)
            print("Public address was saved to file names 'address'.")
        else:
            print("No such file or directory: '" + arg + "'")

    @staticmethod
    def do_new(arg):
        "Get new key pair (private and public)\n\
Save public key to file calls 'compr_compr_pub_key'\n"
        global PRIVATE_KEY
        if PRIVATE_KEY is None:
            PRIVATE_KEY = wallet.get_private_key()
        else:
            get_new = yes_or_no("Private key already exist, do you want generate new one ?")
            if get_new:
                PRIVATE_KEY = wallet.get_private_key()
        print("Private Key: '" + PRIVATE_KEY + "'")
        wallet.get_compressed_public_key(PRIVATE_KEY, 1)
        print("Public key was saved to file names 'compr_pub_key'")

    @staticmethod
    def do_minerkey(arg):
        "Create file with WIF key for mining"
        global PRIVATE_KEY
        if PRIVATE_KEY is None:
            print("Error: private key is missing. Use command 'new' to generate key")
        else:
            PRIVATE_KEY = wallet.get_private_key()
            minerkey = wallet.private_key_to_wif(PRIVATE_KEY, 0, 0)
            f = open("minerkey", "w")
            f.write(minerkey)
            print("Minerkey was created in WIF format and saved to file calls 'minerkey'")
            f.close()


    @staticmethod
    def do_wif(arg):
        "Convert private key to WIF format\n"
        global PRIVATE_KEY
        if PRIVATE_KEY is None:
            print("Error: private key is missing. Use command 'new' to generate key")
        else:
            testnet = yes_or_no("Do you use testnet?")
            compressed = yes_or_no("Use compressed format for WIF?")
            wif = wallet.private_key_to_wif(PRIVATE_KEY, testnet, compressed)
            print("WIF format key: '" + wif + "'")
            # check = yes_or_no("Save WIF key to file calls 'wif_key'?")
            # if check:
            open("wif_key", "w").write(wif)

    @staticmethod
    def do_EOF(arg):
        return True


if __name__ == '__main__':
    PitCoin().cmdloop()
