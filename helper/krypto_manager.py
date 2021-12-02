import hashlib


def hash_str(string, hash_type="sha256"):
    if hash_type == "sha256":
        return hashlib.sha256(string).hexdigest()

def md5(fname):
    image_path = fname
    with open(image_path, 'rb') as image_file:
        image = image_file.read()
    md5 = hashlib.md5()
    md5.update(image)
    hash = md5.digest()
    return hash

class KryptoManager:
    def __init__(self):
        pass
