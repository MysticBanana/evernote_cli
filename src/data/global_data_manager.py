from . import file_loader, user
import os
from helper import krypto_manager, exception
import shutil
import enum

class GlobalFileManager:
    CONSUMER_KEY = None
    CONSUMER_SECRET = None

    class FileManagerError(exception.EvernoteException):
        class ErrorReason(enum.Enum):
            DEFAULT = 1


    def __init__(self, controller):
        self.main_config = file_loader.FileHandler(file_name=".config", mode="json", controller=controller)
        self.controller = controller
        self._credentials = None

    def setup_logging(self):
        self.logger = self.controller.create_logger("DataLoader")

    def init_files(self):
        pathlist = self.get_path()
        for p in pathlist:
            path = pathlist[p]
            if not os.path.exists(path):
                self.logger.warning("File does not exists: " + str(path))
                os.makedirs(path)

        self.CONSUMER_KEY = self.main_config.get("consumer_key")
        self.CONSUMER_SECRET = self.main_config.get("consumer_secret")

        self._credentials = file_loader.FileHandler(file_name=".credentials", mode="json", controller=self.controller)

    def get_api_key(self):
        return self.main_config.get("key")

    def get_path(self, key=None):
        return self.main_config.get("path")[key] if key else self.main_config.get("path")

    def get_user(self, user_name, user_password, token=None, path=False, *args, **kwargs):
        """
        returns relative path to user files or returns UserObject
        :rtype:
        """
        ppath = self.get_path("user_data") + str(user_name) + "/"
        if self.is_user(user_name):
            if path:
                return ppath
            else:
                return user.User(self.controller, ppath, user_name, user_password, token, **kwargs)

    def is_user(self, user_name):
        """
        Checks if user is in .credentials, no check if user files exist
        :param user_name: username
        :return: True if exists
        """
        if user_name in self._credentials.get_all():
            return True
        return False

    def check_user_hash(self, user_name, password_hash):
        """
        :param user_name: username
        :param password_hash: hash of password
        :return:
        """
        up = self._credentials.get(user_name, None)
        if password_hash == up:
            return True
        if up is None:
            self.logger.error("user: {} is not in .credentials".format(user_name))
        return False

    def remove_user(self, user_name):
        """
        Removes the user directory from user_data and removes entry in .credentials
        :param user_name: username
        """
        self.logger.warning("deleting user: %s" % user_name)

        c = self._credentials.get_all()
        c.pop(user_name, None)
        self._credentials.set_all(c)
        self._credentials.dump()

        try:
            shutil.rmtree(u"user_data/{}/".format(user_name))
        except Exception:
            self.logger.error("error while deleting user")
            self.FileManagerError(self.FileManagerError.ErrorReason.DEFAULT, "error while deleting user: %s" % user_name)


    def create_user(self, user_name, user_password, user_password_hash=None, token=None):
        if user_password_hash is None:
            user_password_hash = krypto_manager.hash_str(user_password)

        if self.is_user(user_name):
            self.logger.warning("user already exists")
            return

        path = self.get_path("user_data") + "/" + user_name + "/"

        if os.path.exists(path):
            self.logger.warning("user already exists")
            return

        os.makedirs(path)

        self._credentials.set(user_name, str(user_password_hash))
        self._credentials.dump()

        req = self.main_config.get("user_requirements")
        for file in req:
            if ".json" in file:
                open(path + file, "w").write("{\n}")
            elif "." in file:
                open(path+file, "w").close()
            else:
                os.makedirs(path+file)

        user = self.get_user(user_name, user_password, token=token)
        return user

    def close(self):
        self.main_config.dump()


