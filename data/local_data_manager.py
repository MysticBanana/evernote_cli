from . import file_loader


class UserDataManager:
    def __init__(self, main_class, path, user_name):
        self.user_config = file_loader.Config(config_name=".config", path=path, main_class=main_class)
        self.main_class = main_class

        self.path = path
        self.usr_name = user_name
        self.user_key = "user_key"

        self.logger = self.main_class.create_logger(user_name)


    def __del__(self):
        self.user_config.dump()


