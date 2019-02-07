class Serializer:
    def __init__(self, trans):
        self.tx = '%04x' % trans.amount +\
                  trans.sender +\
                  trans.recipient +\
                  trans.verify_pub_key +\
                  trans.signature

    def get_serialize_tx(self):
        return self.tx


class Deserializer:
    def __init__(self, serial_str):
        self.parameters = {
            'amount': int(serial_str[0:4], 16),
            'sender': serial_str[4:38],
            'recipient': serial_str[38:72],
            'verify_pub_key': serial_str[72:202],
            'signature': serial_str[202:]
        }

    def get_params(self):
        return self.parameters
