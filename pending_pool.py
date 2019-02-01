from tx_validator import validate_tx


def save_transactions(transaction):
    if validate_tx(transaction) is False:
        return False
    file = open("mempool", "a")
    file.write(transaction + '\n')
    file.close()


def return_last_three():
    file = open("mempool", "r")
    transaction_list = file.read().splitlines()
    if len(transaction_list) < 4:
        return transaction_list
    else:
        return transaction_list[-3:]
