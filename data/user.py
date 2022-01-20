# coding=utf-8

import os
import zipfile

import enum

import file_loader
from helper import downloader, exception, krypto_manager, decorator

class User(object):
    # check if bits are set
    class EncryptionLevel(enum.Enum):
        COMPRESS = 0
        ENCRYPT = 1

    class UserError(exception.EvernoteException):
        class ErrorReason(enum.Enum):
            DEFAULT = 1
            INVALID_USERNAME = 2
            INVALID_PASSWORD = 3
            INVALID_TOKEN = 4
            INVALID_ENCRYPTION_LEVEL = 5
            COMPRESSION_ERROR = 6
            ENCRYPTION_ERROR = 7
            CONFIG_MISSING = 8
            DOWNLOAD_ERROR = 9


    def __init__(self, controller, path, user_name, password, token=None, **kwargs):
        self._user_token = token
        self._file_path = ""
        self._encryption_level = 0

        self.user_name = user_name
        self._password = password
        self._password_hash = krypto_manager.hash_str(self._password)

        # if file path does not exists create path for it
        self._force_mode = kwargs.get("force", False)

        self.controller = controller

        self.logger = self.controller.create_logger("USER | %s" % user_name)
        self.logger.info("Initializing user: {}".format(user_name))

        self.km = krypto_manager.CryptoManager(key=self._password, salt="user",
                                               logger=self.controller.create_logger("Krypto"))

        self.user_path = path

        if self._password is None:
            raise self.UserError(self.UserError.ErrorReason.ENCRYPTION_ERROR, "can't encrypt_files with empty password")

        self.user_config = file_loader.FileHandler(file_name=".user_info", path=self.user_path, mode="json", controller=self.controller)
        if not self.user_config.exists:
            raise self.UserError(self.UserError.ErrorReason.CONFIG_MISSING, "Config: .user_info")

        self.decrypt_token()

        self.user_token = self.user_config.get("key") if not self._user_token else self._user_token
        self.file_path = self.user_config.get("file_path", None)
        self.encryption_level = self.user_config.get("encrypt_level", None)

        # if encryption level is set -> decrypt
        self.logger.info("encrypting user files...")
        self.decrypt()

    @property
    def file_path_zip(self):
        return self._file_path[:-1] + ".zip"

    @property
    def user_token(self):
        return self._user_token

    @user_token.setter
    def user_token(self, value):
        try:
            value = unicode(value)
        except Exception:
            raise self.UserError(self.UserError.ErrorReason.INVALID_TOKEN, "can not convert token my bad")

        if type(value) != unicode and type(value) != str:
            raise self.UserError(self.UserError.ErrorReason.INVALID_TOKEN, "token must be unicode (i messed up)")

        if len(value) < 50 > 250 or \
                self.controller.global_data_manager.CONSUMER_KEY not in value:
            raise self.UserError(self.UserError.ErrorReason.INVALID_TOKEN, "token is not the right format")

        self.user_config.set("key", self.encrypt_token(value)).dump()
        self._user_token = value

        self.logger.info("user token set")

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        if value is None:
            self.logger.info("file_path setter is none")
            value = "%sfiles/" % self.user_path

        # checks if valid path
        if os.path.isdir(value) or zipfile.is_zipfile("/".join(value.split("/")[:-2]) + "/files.zip") or self._force_mode:
            if self._force_mode:
                try:
                    os.makedirs(os.path.dirname(value))
                except Exception:
                    raise self.UserError(file_loader.FileHandler.FileHandlerException.ErrorReason.ERROR_CREATING_PATH,
                                         "path: %s " % value)

            self._file_path = value
            self.user_config.set("file_path", self.file_path).dump()

            self.logger.info("custom file path changed")
        # TODO --force einbauen
        else:
            raise self.UserError(self.UserError.ErrorReason.DEFAULT, "path: %s is no dir\n use --force to create this")

    @property
    def max_encryption_level(self):
        return 2 ** len(self.EncryptionLevel) - 1

    @property
    def encryption_level(self):
        return self._encryption_level

    @encryption_level.setter
    def encryption_level(self, value):
        if value is None:
            value = 0

        try:
            value = int(value)
        except Exception:
            raise self.UserError(self.UserError.ErrorReason.INVALID_ENCRYPTION_LEVEL,
                                 "encryption level must be a number: 0-%s" % self.max_encryption_level)

        if value < 0 or value > self.max_encryption_level:
            self.logger.warning("Encryption level is not a proper value and gets set to default 0")
            value = 0

        self._encryption_level = value
        self.user_config.set("encrypt_level", self.encryption_level).dump()
        self.logger.info("encryption level changed")

    @decorator.exception_handler(UserError, "dectypting token", error_reason=UserError.ErrorReason.ENCRYPTION_ERROR)
    def decrypt_token(self):
        token = self.user_config.get("key", None)

        # for other token management
        # if token is None:
        #     raise self.UserError(self.UserError.ErrorReason.DEFAULT, "user token not set")

        if len(str(token)) != 96 and token is not None:
            # set the new encrypted version
            self.user_token = self.km.decrypt_str(token)

    @decorator.exception_handler(UserError, "encrypting token", error_reason=UserError.ErrorReason.ENCRYPTION_ERROR)
    def encrypt_token(self, token=None):
        if token is not None:
            return self.km.encrypt_str(token)

        # if self.user_token != "":
        #     self.user_token = self.km.encrypt_str(self.user_token)
        # else:
        #     raise self.UserError(self.UserError.ErrorReason.ENCRYPTION_ERROR, "user token empty")

    @decorator.exception_handler(UserError, "decrypting files", error_reason=UserError.ErrorReason.ENCRYPTION_ERROR)
    def decrypt_files(self):
        path = self.get_files()

        k = krypto_manager.CryptoManager(self._password)

        for i in path:
            if ".enc" not in i[1]:
                continue
            k.decrypt(i[0], i[1])

        for i in path:
            if ".enc" not in i[1]:
                continue
            os.remove(i[0] + i[1])

    @decorator.exception_handler(UserError, "encrypting files", error_reason=UserError.ErrorReason.ENCRYPTION_ERROR)
    def encrypt_files(self):
        path = self.get_files()

        k = krypto_manager.CryptoManager(self._password)

        for i in path:
            if ".enc" in i[1]:
                continue
            k.encrypt(i[0], i[1])

        for i in path:
            if ".enc" in i[1]:
                continue
            os.remove(i[0].decode('utf-8') + i[1].decode('utf-8'))

    def decrypt(self):
        # handle encryption level
        if bool(self.encryption_level & (1 << self.EncryptionLevel.ENCRYPT.value)):
            self.decrypt_files()
        if bool(self.encryption_level & (1 << self.EncryptionLevel.COMPRESS.value)):
                self.decompress_files()

    def encrypt(self):
        # handle encryption level
        if bool(self.encryption_level & (1 << self.EncryptionLevel.ENCRYPT.value)):
            self.encrypt_files()
        if bool(self.encryption_level & (1 << self.EncryptionLevel.COMPRESS.value)):
            self.compress_files()

    def get_files(self):
        list_of_files = []

        for root, dirs, files in os.walk(self.file_path):
            for f in files:
                list_of_files.append((root.encode('utf-8') + "/", f.encode('utf-8')))

        return list_of_files

    @decorator.exception_handler(UserError, "compressing files", error_reason=UserError.ErrorReason.COMPRESSION_ERROR)
    def compress_files(self):
        path = "/".join(self.file_path.split("/")[:-2]) + "/"
        if os.path.isdir(self.file_path):
            c = krypto_manager.CompressManager()
            c.compress(path, "files")
        else:
            raise self.UserError(self.UserError.ErrorReason.COMPRESSION_ERROR, "path is no dir")

    @decorator.exception_handler(UserError, "decompressing files", error_reason=UserError.ErrorReason.COMPRESSION_ERROR)
    def decompress_files(self):
        path = "/".join(self.file_path.split("/")[:-2]) + "/"
        if os.path.isfile("%sfiles.zip" % path):
            c = krypto_manager.CompressManager()
            c.decompress(path, "files")
        else:
            raise self.UserError(self.UserError.ErrorReason.COMPRESSION_ERROR, "path is no file")

    def save_files(self):
        pass

    def close(self):
        try:
            self.save_files()
        except Exception as e:
            raise self.UserError(self.UserError.ErrorReason.DEFAULT,
                                 "error while saving user files\nS%s" % e)

        self.logger.info("encrypting user files...")
        self.encrypt()

    @decorator.exception_handler(UserError, "downloading user data", error_reason=UserError.ErrorReason.DOWNLOAD_ERROR)
    def download_user_data(self):
        """
        downloads user data and stores it in the .user_info.json of the respective user.
        More user data can be downloaded by expanding the content of the downloaded_data variable
        """
        downloaded_data = ["id", "username", "email", "name", "timezone", "created", "updated", "deleted"]
        d_user = downloader.EvernoteUser(self.controller, self)
        user_info = d_user.get_user_info()
        user_config = self.user_config.get_all()
        user_config[self.user_name] = {}
        for key, val in user_info.items():
            if key in downloaded_data:
                user_config[self.user_name][key] = val
        self.user_config.set_all(user_config)
        self.user_config.dump()

    @decorator.exception_handler(UserError, "downloading notes", error_reason=UserError.ErrorReason.DOWNLOAD_ERROR)
    def test_download(self):
        d = downloader.EvernoteNote(self.controller, self)
        d.download()

    def get_all_files(self):
        files = []
        dirlist = [self.user_path]

        # todo @tom utf-8 codierung hinzufügen! (existiert übrigens schon die gleiche methode)

        while len(dirlist) > 0:
            for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
                dirlist.extend(dirnames)
                files.extend(map(lambda n: os.path.join(*n), zip([dirpath] * len(filenames), filenames)))

        print(files)

if __name__ == "__main__":
    enc_level = 2
    if enc_level > User.EncryptionLevel.COMPRESS:
        pass


