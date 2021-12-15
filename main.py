import sys
import logging
from data import user_data_manager, global_data_manager
import os
from oauth import views
from helper import krypto_manager, displaymanager, param_loader_2

class Evernote:
    def __init__(self, argv=None, **params):
        # loads configs
        self.global_data_manager = global_data_manager.GlobalFileManager(self)

        self.log_level = params.get("log_level", logging.INFO)
        self.setup_logging(level=self.log_level)

        self.logger.info("Starting...")
        self.logger.info("Loaded .user_info.json")

        self.global_data_manager.setup_logging()
        self.global_data_manager.init_files()


        # TESTING
        # User login
        tmp_user_name = "mneuhaus"
        tmp_user_password = "test1234"
        tmp_password_hash = krypto_manager.hash_str(tmp_user_password)

        # CREATING USER
        self.global_data_manager.create_user(tmp_user_name, tmp_password_hash)

        # CHECK LOGIN
        check = self.global_data_manager.check_user_hash(tmp_user_name, tmp_password_hash)
        print check

        # ENCRYPTING USER
        user = self.global_data_manager.get_user(tmp_user_name, tmp_user_password)

        #user.download_user_data()
        # download with key
        #user.test_download()
        # work in progress
        # user.get_all_files()

        # dm = displaymanager.DisplayManager(self)
        # dm.get_dict("-u")

        # par = param_loader_2.ArgumentParser(self, "--user mneuhaus -p test1234 -r a")
        # par.parser()

        #dm = displaymanager.DisplayManager(self)
        #dm.print_help(dict())

        #user_data_manager

    def setup_logging(self, level=logging.INFO):
        """

        :param level:
        """
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')

        path = self.global_data_manager.get_path("log") + "logfile.log"
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path))
            with open(path, "w"):
                pass
        self.log_handler = logging.FileHandler(path)
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

    def user_web_auth(self):
        views.Auth.controller = self
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evernote_oauth.settings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)


# main
if __name__ == "__main__":
    print(sys.argv[1:])

    e = Evernote(sys.argv[1:])
