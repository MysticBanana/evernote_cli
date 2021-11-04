from . import file_loader
import os

class GlobalFileManager:
    def __init__(self, main_class):
        self.main_config = file_loader.Config(config_name=".config", main_class=main_class)
        self.main_class = main_class

    def setup_logging(self):
        self.logger = self.main_class.create_logger("DataLoader")

    def init_files(self):
        pathlist = self.get_path()
        for p in pathlist:
            path = pathlist[p]
            if not os.path.exists(path):
                self.logger.warning("File does not exists: " + str(path))
                os.makedirs(path)

    def get_api_key(self):
        return self.main_config.get("key")

    def get_path(self, key=None):
        return self.main_config.get("path")[key] if key else self.main_config.get("path")

    def get_user(self, user_name, path=True):
        ppath = self.get_path("user_data") + str(user_name)
        if self.is_user(user_name):
            if path:
                return ppath

    def is_user(self, user_name, make_user=False):
        path = self.get_path("user_data") + str(user_name)
        if os.path.exists(path):
            return True
        if make_user:
            self.create_user(user_name)
        return False

    def create_user(self, user_name):
        path = self.get_path("user_data") + str(user_name)
        os.makedirs(path)

        # create user specific config file