from . import file_loader


class Data:
    def __init__(self, main_class):
        self.main_config = file_loader.Config(config_name=".config", main_class=main_class)
        self.main_class = main_class

    def setup_logging(self):
        self.logger = self.main_class.create_logger("DataLoader")

    def get_path(self, key):
        return self.main_config.get("path")[key]