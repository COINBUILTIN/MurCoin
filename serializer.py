class Serializer:
    def __init__(self, trans):
        self.tx = trans.amount.rjust(4)
        self.tx = self.tx + trans.sender.rjust(35)
        self.tx = self.tx + trans.recipient.rjust(35)
        verify_pub_key = trans.ext_pub_key
        self.tx = self.tx + verify_pub_key.rjust(128)
        self.tx = self.tx + trans.signatura

    def get_serial_obj(self):
        return self.tx


class Deserializer:
    def __init__(self, serial_str):
        self.parameters = {
            'amount': serial_str[:4].lstrip('0'),
            'sender': serial_str[4:38].lstrip('0'),
            'recipient': serial_str[38:73].lstrip('0'),
            'verify_pub_key': serial_str[73:201].lstrip('0'),
            'signature': serial_str[201:].lstrip('0')
        }

    def get_params(self):
        return self.parameters
