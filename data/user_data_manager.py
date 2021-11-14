import os

from . import file_loader


class UserDataManager:
    def __init__(self, controller, path, user_name):
        if not os.path.exists(path + "/.config.json"):
            return

        self.user_config = file_loader.Config(config_name=".config", path=path, controller=controller)
        self.user_log = file_loader.Config(config_name="log", path=path, controller=controller, mode="log")

        self.controller = controller
        self.logger = self.controller.create_logger(user_name)
        self.logger.info("Initializing user: {}".format(user_name))

        self.user_path = path
        self.file_path = self.user_path + "/files"
        self.user_name = user_name
        self.user_key = self.user_config.get("key", None)

        # if user wants a custom download location
        custom_file_path = self.user_config.get("file_path", None)
        if custom_file_path:
            self.file_path = custom_file_path
            self.logger.info("File location at: {}".format(custom_file_path))

    def __del__(self):
        self.user_config.dump()
        self.user_log.dump()




