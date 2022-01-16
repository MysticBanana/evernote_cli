import hashlib
import os

from cryptography.fernet import Fernet
import base64
import enum

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from zipfile import ZipFile
import shutil

from helper import exception

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

class CryptoManager:
    class CryptographyError(exception.EvernoteException):
        class ErrorReason(enum.Enum):
            DEFAULT = 1,
            FILE_DOES_NOT_EXIST = 2,
            ERROR_WRITING_IN_FILE = 3,
            ERROR_READING_FILE = 4,
            DECRYPTION_ERROR = 5,
            ENCRYPTION_ERROR = 6

    def __init__(self, key, salt=b"sdffa2edjdh", logger=None):
        salt = salt

        # todo logger
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())

        key = base64.urlsafe_b64encode(kdf.derive(key))

        self.fernet = Fernet(key)

    # todo error catching
    def encrypt(self, file_path, file_name, content_only=False):
        if not os.path.isfile(file_path + file_name):
            print "no file"
            return False

        try:
            if content_only:
                enc_file_name = file_name
            else:
                enc_file_name = self.fernet.encrypt(bytes(file_name))

            with open("{}{}".format(file_path, file_name), "rb") as origin:
                enc_content = origin.read()

            with open("{}{}.enc".format(file_path, enc_file_name), "wb") as encrypted:
                encrypted.write(self.fernet.encrypt(bytes(enc_content)))

            return True
        except Exception as e:
            print e
            # todo error handling
            return False

    def encrypt_str(self, text):
        try:
            return self.fernet.encrypt(bytes(text))
        except Exception as e:
            raise self.CryptographyError(self.CryptographyError.ErrorReason.ENCRYPTION_ERROR,
                                         "Error while encrypting string\n %s" % e)

    def decrypt_str(self, text):
        try:
            return self.fernet.decrypt(bytes(text))
        except Exception as e:
            raise self.CryptographyError(self.CryptographyError.ErrorReason.DECRYPTION_ERROR,
                                         "Error while decrypting string\n %s" % e)

    def decrypt(self, file_path, file_name, content_only=False):
        if not os.path.isfile(file_path + file_name):
            print "no file"
            return

        try:
            if content_only:
                dec_file_name = file_name.replace(".enc", "")
            else:
                dec_file_name = self.fernet.decrypt(file_name)

            with open("{}{}".format(file_path, file_name), "rb") as encrypted:
                dec_content = encrypted.read()

            with open("{}{}".format(file_path, dec_file_name), "wb") as decrypted:
                decrypted.write(self.fernet.decrypt(dec_content))

            return True

        except Exception as e:
            print e
            # todo error handling
            return False


class CompressManager():
    def __init__(self, logger=None):
        pass

    def compress(self, path, file):
        complet_path = "{}/{}".format(path, file)
        shutil.make_archive(complet_path, "zip", complet_path)
        shutil.rmtree("{}/{}".format(path, file))

    def decompress(self, path, file):
        complet_path = "{}/{}".format(path, file)
        with ZipFile("{}.zip".format(complet_path), "r") as zipObj:
            zipObj.extractall(complet_path)
        os.remove("{}.zip".format(complet_path))


if __name__ == "__main__":
    print hash_str("passwd123")
