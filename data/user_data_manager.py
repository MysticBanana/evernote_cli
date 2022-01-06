import os
import enum

from . import file_loader
from helper import downloader, krypto_manager
import file_loader
from helper import downloader



class UserDataManager(object):
    class EncryptionLevel(enum.Enum):
        DEFAULT = 0
        COMPRESS = 1
        ENCRYPT = 2
        COMPRESS_ENCRYPT = 4

    def __init__(self, controller, path, user_name, password):
        # todo: set option in user_info for encryption_level

        self.controller = controller
        self.logger = self.controller.create_logger(user_name)
        self.logger.info("Initializing user: {}".format(user_name))

        self.user_path = path
        self.file_path = "%sfiles/" % self.user_path
        self.file_path_zip = self.file_path[:len(self.file_path)-1] + ".zip"
        self.user_name = user_name
        self.user_password = password

        self.user_config = file_loader.FileHandler(file_name=".user_info", path=self.user_path, mode="json", controller=self.controller)
        self.user_log = None
        self.user_key = None
        self.password = password

        if not self.user_config.exists:
            return

        self.init_files()

        # user decryption
        # if self.encryption_level > 1:
        #     self.decrypt()



        # self.get_files(self.encrypt)

    @property
    def user_token(self):
        return self.user_key

    @user_token.setter
    def user_token(self, value):
        self.user_config.set("key", str(value))
        self.user_config.set("file_path", self.file_path)
        self.user_config.set("encrypt_lvl", self.encryption_level)
        self.user_config.dump()
        self.user_key = value


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

        k = krypto_manager.KryptoManager(self.user_password)

        for i in path:
            k.decrypt(i[0], i[1])

        for i in path:
            os.remove(i[0] + i[1])

    def encrypt(self):
        path = self.get_files()

        k = krypto_manager.KryptoManager(self.user_password)

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
        if self.encryption_level > self.EncryptionLevel.ENCRYPT:
            self.encrypt()
            self.compress()
        elif self.encryption_level > self.EncryptionLevel.COMPRESS:
            self.encrypt()
        elif self.encryption_level > self.EncryptionLevel.DEFAULT:
            self.compress()

    def set_custom_path(self, path):
        # check if path valid
        if os.path.isdir(path) or path.endswith(".zip"):
            self.user_config.set("file_path", path)
            self.file_path = path
            self.file_path_zip = path[:len(self.file_path)-1] + ".zip"
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
    if enc_level > UserDataManager.EncryptionLevel.COMPRESS:
        pass


