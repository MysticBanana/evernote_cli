import sys
import logging
from data import data


class Evernote:
    def __init__(self, argv=None, **params):
        # loads configs
        self.data_manager = data.Data(self)

        self.log_level = params.get("log_level", logging.INFO)
        self.setup_logging(level=self.log_level)

        self.logger.info("Starting...")
        self.logger.info("Loaded .config.json")

        self.data_manager.setup_logging()

        if not argv:
            pass
            # log error

    def setup_logging(self, logger_name="None", level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')

        self.log_handler = logging.FileHandler(self.data_manager.get_path("log") + "logfile.log")
        self.log_handler.setFormatter(formatter)

        self.logger = logging.getLogger("Main")
        self.logger.setLevel(level)
        self.logger.addHandler(self.log_handler)

    def get_logger(self):
        return self.logger

    def get_log_handler(self):
        return self.log_handler

    def create_logger(self, name):
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
        print(error_message)
        exit()


if __name__ == "__main__":
    print(sys.argv[1:])

    e = Evernote(sys.argv[1:])
    e.get_logger().log(msg="logpath works", level=logging.INFO)

