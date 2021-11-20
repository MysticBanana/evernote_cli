from hashlib import sha256


def hash_str(string):
    return sha256(string).hexdigest()

class KryptoManager:
    def __init__(self):
        pass

