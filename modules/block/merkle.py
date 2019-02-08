from hashlib import sha256


def merkle_tree(tx_list):
    new_tx_list = []
    while len(tx_list) < 4:
        tx_list.append(tx_list[-1])
    for tx in tx_list:
        hash_tx = sha256(tx.encode("utf-8")).hexdigest()
        new_tx_list.append(hash_tx)
    return get_merkle_root(new_tx_list)


def get_merkle_root(tx_list):
    if len(tx_list) == 1:
        return tx_list[0]
    new_tx_list = []
    if len(tx_list) % 2 == 1:
        tx_list.append(tx_list[-1])
    for i in range(0, len(tx_list)-1, 2):
        new_tx_list.append(double_hash(tx_list[i], tx_list[i+1]))
    return get_merkle_root(new_tx_list)


def double_hash(first, second):
    sums = first + second
    res = sha256(sha256(sums.encode("utf-8")).digest()).hexdigest()
    return res
