import hashlib
import os

import stdiomask as stdiomask
from cryptography.fernet import Fernet
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from zipfile import ZipFile


def hash_str(string, hash_type="sha256"):
    if hash_type == "sha256":
        return hashlib.sha256(string).hexdigest()
    elif hash_type == "md5":
        return hashlib.md5(string).hexdigest()


def file_hash(file_path, hash_type="sha256"):
    with open(file_path, "rb") as _file:
        content = _file.read()

    if hash_type == "sha256":
        hash_type = hashlib.sha256()

    elif hash_type == "md5":
        hash_type = hashlib.md5()

    else:
        return False

    hash_type.update(content)
    return hash_type.digest()


def md5(fname):
    image_path = fname
    with open(image_path, 'rb') as image_file:
        image = image_file.read()
    md5 = hashlib.md5()
    md5.update(image)
    hash = md5.digest()
    return hash


class KryptoManager:
    def __init__(self, key):
        salt = b"sdffa2edjdh"

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())

        key = base64.urlsafe_b64encode(kdf.derive(key))

        self.fernet = Fernet(key)

    def encrypt(self, file_path, file_name):
        if not os.path.isfile(file_path + file_name):
            print "no file"
            return

        enc_file_name = self.fernet.encrypt(bytes(file_name))

        with open("{}{}".format(file_path, file_name), "rb") as origin:
            enc_content = origin.read()

        with open("{}{}.enc".format(file_path, enc_file_name), "wb") as encrypted:
            encrypted.write(self.fernet.encrypt(bytes(enc_content)))

    def decrypt(self, file_path, file_name):
        if not os.path.isfile(file_path + file_name):
            print "no file"
            return

        dec_file_name = self.fernet.decrypt(file_name)

        with open("{}{}".format(file_path, file_name), "rb") as encrypted:
            dec_content = encrypted.read()

        with open("{}{}".format(file_path, dec_file_name), "wb") as decrypted:
            decrypted.write(self.fernet.decrypt(dec_content))


class CompressManager():
    def __init__(self, controller, username, password):
        self.controller = controller
        self.user = self.controller.global_data_manager.get_user(username, password)
        self.path = self.user.file_path
        self.path_zip = self.user.file_path_zip

    def compress(self):
        with ZipFile(self.path_zip, "w") as zipObj:
            zipObj.write(self.path) # zipping dir
        os.remove(self.path)

    def decompress(self):
        with ZipFile(self.path_zip, "r") as zipObj:
            zipObj.extract(self.path)
        #os.remove(self.path_zip)



if __name__ == "__main__":
    key = b"password1234"
    # print base64.urlsafe_b64encode(key)
    k = KryptoManager(key)
    # k.encrypt("", "test_file.txt")
    k.decrypt("",
              "gAAAAABhtU3TIbc6xf_LXW40a8WkTPQl2HbO3fh8MpRnlIn3HkaNpQrN3Pvm7P87SoWv4HHj6Drkdo6GkhXV_TcUP7zY9DK4fw==.enc")
