import sys
import logging
import evernote


class Evernote:
    def __init__(self, argv=None, **params):
        self.log_level = params.get("log_level", logging.INFO)
        self.setup_logging(level=self.log_level)



        if not argv:
            pass
            # log error

    def setup_logging(self, logger_name="None", level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')

        # hardcoded log path
        self.log_handler = logging.FileHandler("logs/logfile.log")
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
        pass


if __name__ == "__main__":
    print(sys.argv[1:])

    e = Evernote(sys.argv[1:])
    e.get_logger().log(msg="test", level=logging.INFO)

