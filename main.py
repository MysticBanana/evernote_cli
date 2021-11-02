import sys
import logging
from data import local_data_manager, global_data_manager


class Evernote:
    def __init__(self, argv=None, **params):
        # loads configs
        self.global_data_manager = global_data_manager.GlobalFileManager(self)

        self.log_level = params.get("log_level", logging.INFO)
        self.setup_logging(level=self.log_level)

        self.logger.info("Starting...")
        self.logger.info("Loaded .config.json")

        self.global_data_manager.setup_logging()
        self.global_data_manager.init_files()

        if not argv:
            pass
            # log error

    def setup_logging(self, level=logging.INFO):
        """

        :param level:
        """
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')

        self.log_handler = logging.FileHandler(self.global_data_manager.get_path("log") + "logfile.log")
        self.log_handler.setFormatter(formatter)

        self.logger = logging.getLogger("Main")
        self.logger.setLevel(level)
        self.logger.addHandler(self.log_handler)

    def get_logger(self):
        return self.logger

    def get_log_handler(self):
        return self.log_handler

    def create_logger(self, name):
        """

        :param name:
        :return:
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        logger.addHandler(self.log_handler)
        return logger

    def exit_error(self, error_message=None):
        """
        Call this function when error appeared. Prints error to commandline and logs in log files
        :param error_message:
        """
        # close and exit all services now

        if hasattr(self, "logger"):
            self.logger.error(msg=error_message)
        print error_message
        exit()


if __name__ == "__main__":
    print(sys.argv[1:])

    e = Evernote(sys.argv[1:])

