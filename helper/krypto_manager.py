from hashlib import sha256


def hash_str(string, hash_type="sha256"):
    if hash_type == "sha256":
        return sha256(string).hexdigest()

class KryptoManager:
    def __init__(self):
        pass

