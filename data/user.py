import os
import enum

from . import file_loader
from helper import downloader, krypto_manager
import file_loader
from helper import downloader

class User(object):
    class EncryptionLevel(enum.Enum):
        DEFAULT = 1
        COMPRESS = 2
        ENCRYPT = 3
        COMPRESS_ENCRYPT = 6

    def __init__(self, controller, path, user_name, password):
        self._user_key = None
        self._file_path = ""
        self._encryption_level = self.EncryptionLevel.DEFAULT

        self.user_name = user_name
        self._password = password
        # todo
        self._password_hash = krypto_manager.hash_str(self._password)

        self.controller = controller

        self.logger = self.controller.create_logger(user_name)
        self.logger.info("Initializing user: {}".format(user_name))

        self.user_path = path
        # todo filepath auch zu begin mit in die config schreiben


        self.decrypt_info()

        self.user_config = file_loader.FileHandler(file_name=".user_info", path=self.user_path, mode="json", controller=self.controller)
        if not self.user_config.exists:
            # todo error handling
            print "user_config does not exist"
            return

        self._user_key = self.user_config.get("key")
        self._file_path = self.user_config.get("file_path", None)
        if self._file_path is None:
            self._file_path = "%sfiles/" % self.user_path
        enc_level = self.user_config.get("encrypt_level", None)
        if enc_level is not None:
            self.encryption_level = enc_level


    @property
    def file_path_zip(self):
        return self._file_path[:-1] + ".zip"

    @property
    def user_token(self):
        return self.user_key

    @user_token.setter
    def user_token(self, value):
        self.user_config.set("key", str(value))
        self.user_config.dump()
        self.user_key = value

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value
        self.user_config.set("file_path", self.file_path)
        self.user_config.dump()

    @property
    def encryption_level(self):
        return self._encryption_level

    @encryption_level.setter
    def encryption_level(self, value):
        self._encryption_level = value
        # todo work around with enum


        self.user_config.set("encrypt_level", self.encryption_level)
        self.user_config.dump()

    def decrypt_info(self):
        _file_name = ".user_info.json.enc"
        self.km = krypto_manager.KryptoManager(key=self._password, salt="user",
                                               logger=self.controller.create_logger("Krypto"))

        if not os.path.isfile(self.user_path + _file_name):
            return

        success = self.km.decrypt(file_path=self.user_path, file_name=_file_name, content_only=True)
        if success:
            os.remove(self.user_path + _file_name)

    def init_files(self):
        #self.user_log = file_loader.FileHandler(file_name="log", path=self.user_path, controller=self.controller, mode="json", mode="log")
        self.user_key = self.user_config.get("key", None)
        self.encryption_level = 2

        # if user wants a custom download location
        custom_file_path = self.user_config.get("file_path", "")
        if custom_file_path:
            self.file_path = custom_file_path
            self.logger.info("File location at: {}".format(custom_file_path))

    def dump_config(self):
        self.user_config.set("key", self.user_key)

    def decrypt(self):
        path = self.get_files()

        k = krypto_manager.KryptoManager(self._password)

        for i in path:
            k.decrypt(i[0], i[1])

        for i in path:
            os.remove(i[0] + i[1])

    def encrypt(self):
        path = self.get_files()

        k = krypto_manager.KryptoManager(self._password)

        for i in path:
            k.encrypt(i[0], i[1])

        for i in path:
            os.remove(i[0].decode('utf-8') + i[1].decode('utf-8'))

    def get_files(self):

        # k = krypto_manager.KryptoManager(self.user_password)

        list_of_files = []

        for root, dirs, files in os.walk(self.file_path):
            for f in files:
                list_of_files.append((root.encode('utf-8') + "/", f.encode('utf-8')))

        return list_of_files

    def compress(self):
        pass

    def decompress(self):
        pass

    def close(self):
        self.user_config.dump()

        if self._password is not None:
            success = self.km.encrypt(self.user_path, file_name=".user_info.json", content_only=True)
            if success:
                os.remove(self.user_path + ".user_info.json")

        # if self.encryption_level > self.EncryptionLevel.ENCRYPT:
        #     self.encrypt()
        #     self.compress()
        # elif self.encryption_level > self.EncryptionLevel.COMPRESS:
        #     self.encrypt()
        # elif self.encryption_level > self.EncryptionLevel.DEFAULT:
        #     self.compress()




    def set_custom_path(self, path):
        # check if path valid
        if os.path.isdir(path) or path.endswith(".zip"):
            self.user_config.set("file_path", path)
            self.file_path = path
            self.user_config.dump()
        else:
            print "Path is no Dir"
            # TODO: Error ausgeben
            # TODO: In property umwandeln

    def set_encryption_lvl(self, encrypt_lvl):
        self.encryption_level = encrypt_lvl
        self.user_config.set("encrypt_lvl", self.encryption_level)
        self.user_config.dump()

    # downloads user data and stores it in the .user_info.json of the respective user.
    # More user data can be downloaded by expanding the content of the downloaded_data variable
    def download_user_data(self):
        downloaded_data = ["id", "username", "email", "name", "timezone", "created", "updated", "deleted"]
        d_user = downloader.EvernoteUser(self)
        user_info = d_user.get_user_info()
        user_config = self.user_config.get_all()
        user_config[self.user_name] = {}
        for key, val in user_info.items():
            if key in downloaded_data:
                user_config[self.user_name][key] = val
        self.user_config.set_all(user_config)
        self.user_config.dump()

    def test_download(self):
        d = downloader.EvernoteNote(self)
        d.download()
        # downloader.downloadstart(self.user_key)

    def get_all_files(self):
        files = []
        dirlist = [self.user_path]

        while len(dirlist) > 0:
            for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
                dirlist.extend(dirnames)
                files.extend(map(lambda n: os.path.join(*n), zip([dirpath] * len(filenames), filenames)))

        print(files)

if __name__ == "__main__":
    enc_level = 2
    if enc_level > User.EncryptionLevel.COMPRESS:
        pass

