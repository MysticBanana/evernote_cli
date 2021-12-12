from . import file_loader, user_data_manager
import os

class GlobalFileManager:
    def __init__(self, controller):
        self.main_config = file_loader.FileHandler(file_name=".config", controller=controller)
        self.controller = controller

    def setup_logging(self):
        self.logger = self.controller.create_logger("DataLoader")

    def init_files(self):
        pathlist = self.get_path()
        for p in pathlist:
            path = pathlist[p]
            if not os.path.exists(path):
                self.logger.warning("File does not exists: " + str(path))
                os.makedirs(path)

        self.credentials = file_loader.FileHandler(file_name=".credentials", controller=self.controller)

    def get_api_key(self):
        return self.main_config.get("key")

    def get_path(self, key=None):
        return self.main_config.get("path")[key] if key else self.main_config.get("path")

    def get_user(self, user_name, user_password, path=False):
        """
        returns relative path to user files or returns UserObject
        :rtype:
        """
        ppath = self.get_path("user_data") + str(user_name) + "/"
        if self.is_user(user_name):
            if path:
                return ppath
            else:
                return user_data_manager.UserDataManager(self.controller, ppath, user_name, user_password)

    def is_user(self, user_name):
        if user_name in self.credentials.getAll():
            return True
        return False

    def check_user_hash(self, user_name, password_hash):
        up = self.credentials.get(user_name, None)
        if password_hash == up:
            return True
        if up is None:
            self.logger.error("user: {} is not in .credentials".format(user_name))
        return False

    def create_user(self, user_name, password_hash):
        if self.is_user(user_name):
            return
        path = self.get_path("user_data") + "/" + str(user_name) + "/"
        os.makedirs(path)
        self.credentials.set(user_name, str(password_hash))
        self.credentials.dump()

        req = self.main_config.get("user_requirements")
        for file in req:
            if ".json" in file:
                open(path + file, "w").write("{\n}")
            elif "." in file:
                open(path+file, "w").close()
            else:
                os.makedirs(path+file)


        # create user specific config file