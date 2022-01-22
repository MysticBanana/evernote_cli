import base64
import hashlib
import os
import shutil
from zipfile import ZipFile
from time import sleep

import enum
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from helper import exception, decorator


def hash_str(string, hash_type="sha256"):
    """
    Calculate the hash of a string
    :param string: string to hash
    :param hash_type: hash methode to use, default is sha256
    :return: retuns the hash string
    """
    if hash_type == "sha256":
        return hashlib.sha256(string).hexdigest()
    elif hash_type == "md5":
        return hashlib.md5(string).hexdigest()


def file_hash(file_path, hash_type="sha256"):
    """
    Calculate the hash of a file
    :param file_path: the absolute or relative path to the file
    :param hash_type: hash methode to use, default is sha256
    :return: returns the hash string
    """
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
        """
        Generate a fernet object for decryption and encryption
        :param key: the key to encrypt with
        :param salt: salt for encryption
        :param logger: logger object (optional)
        """
        salt = salt

        # todo logger
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())

        key = base64.urlsafe_b64encode(kdf.derive(key))

        self.logger = logger
        self.fernet = Fernet(key)

    @decorator.exception_handler(CryptographyError, "error while encrypting file",
                                 error_reason=CryptographyError.ErrorReason.ENCRYPTION_ERROR)
    def encrypt(self, file_path, file_name, content_only=False):
        """
        Encrypting the file content and name, adds '.enc' at the end
        :param file_path: path to the file (ends with '/')
        :param file_name: name of the file to encrypt
        :param content_only: if filename should not be changed
        :return: True if encryption was successful
        """
        if not os.path.isfile(file_path + file_name):
            if self.logger:
                self.logger.error("no file found for encryption")

        if content_only:
            enc_file_name = file_name
        else:
            enc_file_name = self.fernet.encrypt(bytes(file_name))

        with open("{}{}".format(file_path, file_name), "rb") as origin:
            enc_content = origin.read()

        with open("{}{}.enc".format(file_path, enc_file_name), "wb") as encrypted:
            encrypted.write(self.fernet.encrypt(bytes(enc_content)))

        return True

    def encrypt_str(self, text):
        """
        Encryption of a string
        :param text: text string to get encrypted
        :return: returns the encrypted string
        """
        try:
            return self.fernet.encrypt(bytes(text))
        except Exception as e:
            raise self.CryptographyError(self.CryptographyError.ErrorReason.ENCRYPTION_ERROR,
                                         "Error while encrypting string\n %s" % e)

    # TODO decorator
    def decrypt_str(self, text):
        """
        Decryption of a string
        :param text: text string to get decrypted
        :return: returns the decrypted string
        """
        try:
            return self.fernet.decrypt(bytes(text))
        except Exception as e:
            raise self.CryptographyError(self.CryptographyError.ErrorReason.DECRYPTION_ERROR,
                                         "Error while decrypting string\n %s" % e)

    @decorator.exception_handler(CryptographyError, "error while decrypting file",
                                 error_reason=CryptographyError.ErrorReason.DECRYPTION_ERROR)
    def decrypt(self, file_path, file_name, content_only=False):
        """
        Decrypting the file content and name, removes '.enc' if in the filename
        :param file_path: path to the file (ends with '/')
        :param file_name: name of the file to decrypt
        :param content_only: if filename should not be changed
        :return: True if decryption was successful
        """
        if not os.path.isfile(file_path + file_name):
            if self.logger:
                self.logger.error("no file found for decryption")

        if content_only:
            dec_file_name = file_name.replace(".enc", "")
        else:
            dec_file_name = self.fernet.decrypt(file_name)

        with open("{}{}".format(file_path, file_name), "rb") as encrypted:
            dec_content = encrypted.read()

        with open("{}{}".format(file_path, dec_file_name), "wb") as decrypted:
            decrypted.write(self.fernet.decrypt(dec_content))

        return True

class CompressManager():
    def __init__(self, logger=None):
        self.logger = logger

    def compress(self, path, file):
        """
        Zipping a file and removing the directory
        :param path: path to file (not necessary to end with '/')
        :param file: filename
        """
        complet_path = "{}/{}".format(path, file)
        shutil.make_archive(complet_path, "zip", complet_path)
        shutil.rmtree("{}/{}".format(path, file))

    def decompress(self, path, file):
        """
        Extracting a zip archive and removing the .zip at the end
        :param path: path to file (not necessary to end with '/')
        :param file: filename
        """
        complet_path = "{}/{}".format(path, file)
        with ZipFile("{}.zip".format(complet_path), "r") as zipObj:
            zipObj.extractall(complet_path)

        # need a sleep otherwise raise error because file isnt closed
        sleep(1)
        os.remove("{}.zip".format(complet_path))


if __name__ == "__main__":
    print hash_str("passwd123")
