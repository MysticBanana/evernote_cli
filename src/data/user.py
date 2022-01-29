# coding=utf-8

import os
import shutil
import zipfile
from time import sleep
from datetime import datetime
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

    # default values for settings
    defaults = {
        "overwrite_files": False,
        "create_download_path": False
    }

    def __init__(self, controller, path, user_name, password, token=None, **kwargs):
        """
        Initialise user

        Gets data from .user_info and if values arnt set, set them to default values.
        Checks if all dirs and needed files exist in user directory and creates them if not.
        Decrypt user files.
        :param controller: instance of the Evernote object
        :param path: path of the root user dir - user_data/
        :param token: access token for authentication with evernote API
        """
        self._user_token = token
        self._file_path = ""
        self._encryption_level = 0

        self.user_name = user_name
        self._password = password
        self._password_hash = krypto_manager.hash_str(self._password)

        # if file path does not exists create path for it
        self._force_mode = kwargs.get("force_mode", False)
        self._overwrite = kwargs.get("overwrite", False)  # replace with just force maybe?

        self.controller = controller

        self.logger = self.controller.create_logger("USER | %s" % user_name)
        self.logger.info("Initializing user: {}".format(user_name))

        # self.decrypt_token()
        self.km = krypto_manager.CryptoManager(key=self._password, salt="user",
                                               logger=self.controller.create_logger("Krypto"))
        self.user_path = path

        if self._password is None:
            raise self.UserError(self.UserError.ErrorReason.ENCRYPTION_ERROR, "can't encrypt_files with empty password")

        self.user_config = file_loader.FileHandler(file_name=".user_info", path=self.user_path, mode="json",
                                                   controller=self.controller)
        if not self.user_config.exists:
            raise self.UserError(self.UserError.ErrorReason.CONFIG_MISSING, "Config: .user_info")

        self.decrypt_token()

        self.user_token = self.user_config.get("key") if not self._user_token else self._user_token
        self.file_path = self.user_config.get("file_path", None)
        self.encryption_level = self.user_config.get("encrypt_level", None)

        # defaults
        d = self.user_config.get("file_path", None)
        if d is None:
            self.defaults = d
        else:
            self.user_config.set("defaults", self.defaults)

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
        """
        checks correctness of token and save it in .user_info
        :param value:
        """
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
        """
        returns the path where to save downloaded files
        """
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        """
        checks correctness of path and save it in .user_info
        """
        if value is None:
            self.logger.info("file_path setter is none")
            value = "%sfiles" % self.user_path

        # checks if valid path
        if os.path.isdir(value) or zipfile.is_zipfile(
                "{dirname}/{name}.zip".format(dirname=os.path.dirname(value), name=os.path.basename(value))) or self._force_mode or self._overwrite or self.defaults[
            "create_download_path"]:
            if self._force_mode or self._overwrite or self.defaults["create_download_path"]:
                try:
                    if not os.path.isdir(value):
                        os.makedirs(os.path.dirname(value))
                except Exception:
                    raise self.UserError(file_loader.FileHandler.FileHandlerException.ErrorReason.ERROR_CREATING_PATH,
                                         "path: %s " % value)

            value = value[:-1] if (value[-1] == "/") else value

            self._file_path = value
            self.user_config.set("file_path", self.file_path).dump()

            self.logger.info("custom file path changed")
        # TODO --force einbauen
        else:
            raise self.UserError(self.UserError.ErrorReason.DEFAULT,
                                 "path: %s is no dir\n use --force or --overwrite to create it")

    @property
    def max_encryption_level(self):
        """
        returns max encryption level possible
        """
        return 2 ** len(self.EncryptionLevel) - 1

    @property
    def encryption_level(self):
        return self._encryption_level

    @encryption_level.setter
    def encryption_level(self, value):
        """
        checks correctness of path and save it in .user_info
        """
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

    @property
    def overwrite(self):
        return self._overwrite

    @property
    def force_mode(self):
        return self._force_mode

    def get_default(self, default):
        return self.defaults.get(default, False)

    @decorator.exception_handler(UserError, "decrypting token", error_reason=UserError.ErrorReason.ENCRYPTION_ERROR)
    def decrypt_token(self):
        """
        gets token from .user_info and returns it decrypted
        """
        token = self.user_config.get("key", None)
        if len(str(token)) != 96 and token is not None:
            # set the new encrypted version
            self.user_token = self.km.decrypt_str(token)

    @decorator.exception_handler(UserError, "encrypting token", error_reason=UserError.ErrorReason.ENCRYPTION_ERROR)
    def encrypt_token(self, token=None):
        """
        returns a encrypted token
        """
        if token is not None:
            return self.km.encrypt_str(token)

    @decorator.exception_handler(UserError, "decrypting files", error_reason=UserError.ErrorReason.ENCRYPTION_ERROR)
    def decrypt_files(self):
        """
        iterate through downloaded files, decrypt them and deletes encrypted files after
        """
        path = self.get_files()

        k = krypto_manager.CryptoManager(self._password)

        enc_names = self.user_config.get("encrypted_names", {})
        if not len(enc_names):
            return

        for i in path:
            if ".enc" not in i[1]:
                continue
            k.decrypt(i[0], i[1], origin_name=enc_names.get(i[1].replace(".enc", "")))

        self.user_config.set("encrypted_names", {})

        for i in path:
            if ".enc" not in i[1]:
                continue
            os.remove(unicode(i[0]) + unicode(i[1]))

    @decorator.exception_handler(UserError, "encrypting files", error_reason=UserError.ErrorReason.ENCRYPTION_ERROR)
    def encrypt_files(self):
        """
        iterate through downloaded files, encrypt them and deletes files after
        """
        path = self.get_files()

        k = krypto_manager.CryptoManager(self._password)

        enc_names = {}

        for i in path:
            if ".enc" in i[1]:
                continue
            names = k.encrypt(i[0], i[1])
            enc_names[names[0]] = names[1]

        self.user_config.set("encrypted_names", enc_names)
        self.user_config.dump()

        for i in path:
            if ".enc" in i[1]:
                continue
            os.remove(i[0].decode('utf-8') + i[1].decode('utf-8'))

    def decrypt(self):
        """
        Calls functions selected from encryption level to decrypt/uncompress files
        """
        # handle encryption level
        if bool(self.encryption_level & (1 << self.EncryptionLevel.COMPRESS.value)):
            self.decompress_files()
        if bool(self.encryption_level & (1 << self.EncryptionLevel.ENCRYPT.value)):
            self.decrypt_files()

    def encrypt(self):
        """
        Calls functions selected from encryption level to encrypt/compress files
        """
        # handle encryption level
        if bool(self.encryption_level & (1 << self.EncryptionLevel.ENCRYPT.value)):
            self.encrypt_files()
        if bool(self.encryption_level & (1 << self.EncryptionLevel.COMPRESS.value)):
            self.compress_files()

    def get_files(self, path=None):
        """
        Returns a list of all files (path + file) in <path>
        """
        list_of_files = []
        for root, dirs, files in os.walk(path or self.file_path):
            for f in files:
                list_of_files.append((root.encode('utf-8') + "/", f.encode('utf-8')))

        return list_of_files

    @decorator.exception_handler(UserError, "compressing files", error_reason=UserError.ErrorReason.COMPRESSION_ERROR)
    def compress_files(self):
        """
        Makes a zip archive from all files in download directory
        """
        # path = os.path.abspath(os.path.join(self.file_path, '..'))
        path = os.path.dirname(self.file_path)

        if os.path.isdir(self.file_path):
            c = krypto_manager.CompressManager(dst=u"{}/{}.zip".format(path, os.path.basename(self.file_path)))
            c.compress(self.file_path)
            c.close()

            del c
            sleep(1)

            try:
                shutil.rmtree(u"{}/{}".format(path, os.path.basename(self.file_path)))
            except WindowsError:
                # folder is still opened and avoid access denied
                pass
        else:
            raise self.UserError(self.UserError.ErrorReason.COMPRESSION_ERROR, "path is no dir")

    @decorator.exception_handler(UserError, "decompressing files", error_reason=UserError.ErrorReason.COMPRESSION_ERROR)
    def decompress_files(self):
        """
        Extract all files from the zip archive
        """

        path = os.path.dirname(self.file_path)
        try:
            if os.path.isfile(u"{path}/{filename}.zip".format(path=path, filename=os.path.basename(self.file_path))):
                c = krypto_manager.CompressManager()
                c.decompress(path, u"{}.zip".format(os.path.basename(self.file_path)))
            else:
                return
                # should be ignored if deleted or moved
                # raise self.UserError(self.UserError.ErrorReason.COMPRESSION_ERROR, "path is no file")
        except IOError as e:
            print "im sorry i dont have permission for this"
            self.logger.error("no permission to access the zip")
            raise e

    def save_files(self):
        pass

    def close(self):
        """
        Called at the end of the program to close/save all config files.
        Encrypt downloaded files.
        """
        try:
            self.save_files()
            self.user_token = self._user_token
        except Exception as e:
            raise self.UserError(self.UserError.ErrorReason.DEFAULT,
                                 "error while saving user files\nS%s" % e)

        self.logger.info("encrypting user files...")
        self.encrypt()

    @decorator.exception_handler(UserError, "downloading user data", error_reason=UserError.ErrorReason.DOWNLOAD_ERROR)
    def download_user_data(self):
        """
        Downloads user data and stores it in the .user_info.json of the respective user.
        More user data can be downloaded by expanding the content of the downloaded_data variable
        """
        downloaded_data = ["id", "username", "email", "name", "timezone", "created", "updated", "deleted"]
        times = ["created", "updated", "deleted"]
        d_user = downloader.EvernoteUser(self.controller, self)
        user_info = d_user.get_user_info()
        user_config = self.user_config.get_all()
        user_config[self.user_name] = {}
        for key, val in user_info.items():
            if key in downloaded_data:
                user_config[self.user_name][key] = val
            if key in times and val is not None:
                user_config[self.user_name][key] = datetime.fromtimestamp(val / 1000).strftime("%A, %B %d, %Y %H:%M:%S")

        self.user_config.set_all(user_config)
        self.user_config.dump()

    @decorator.exception_handler(UserError, "downloading notes", error_reason=UserError.ErrorReason.DOWNLOAD_ERROR)
    def test_download(self):
        """
        Downloads all files from cloud storage and saves to self.file_path
        """
        d = downloader.EvernoteNote(self.controller, self)
        d.download()