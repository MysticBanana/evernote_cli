import sys
import logging


class Evernote:
    def __init__(self, argv=None, **params):





        if not argv:
            pass
            # log error

    def logger(self, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        loggers = {
            "network": None,
            "file_manager": None
        }

        # handler = logging.FileHandler(log_file)
        # handler.setFormatter(formatter)
        #
        # logger = logging.getLogger(name)
        # logger.setLevel(level)
        # logger.addHandler(handler)

    def exit_error(self, error_message=None):
        """
        Call this function when error appeared. Prints error to commandline and logs in log files
        :param error_message:
        """
        pass


if __name__ == "__main__":
    print(sys.argv)
