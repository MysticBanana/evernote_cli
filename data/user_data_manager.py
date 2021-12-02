import os

from . import file_loader
from helper import downloader

class UserDataManager:
    def __init__(self, controller, path, user_name):
        self.controller = controller
        self.logger = self.controller.create_logger(user_name)
        self.logger.info("Initializing user: {}".format(user_name))

        self.user_path = path
        self.file_path = "%s/files" % self.user_path
        self.user_name = user_name

        self.user_config = None
        self.user_log = None
        self.user_key = None

        if not os.path.exists("%s/.user_info.json" % self.user_path):
            return

        self.init_files()

    def init_files(self):
        self.user_config = file_loader.Config(config_name=".config", path=self.user_path, controller=self.controller)
        self.user_log = file_loader.Config(config_name="log", path=self.user_path, controller=self.controller, mode="log")
        self.user_key = self.user_config.get("key", None)

        # if user wants a custom download location
        custom_file_path = self.user_config.get("file_path", None)
        if custom_file_path:
            self.file_path = custom_file_path
            self.logger.info("File location at: {}".format(custom_file_path))

    def decrypt(self):
        pass

    def encrypt(self):
        pass

    def set_custom_path(self, path):
        # check if path valid
        if os.path.isdir(path):
            self.user_config.set("file_path", path)
            self.file_path = path
        else:
            print "Path is no Dir"
            # TODO: Error ausgeben

    def test_download(self):
        downloader.downloadstart(self.user_key)

    def get_all_files(self):
        files = []
        dirlist = [self.user_path]

        while len(dirlist) > 0:
            for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
                dirlist.extend(dirnames)
                files.extend(map(lambda n: os.path.join(*n), zip([dirpath] * len(filenames), filenames)))

        print(files)

    def __del__(self):
        pass #self.user_config.dump()




