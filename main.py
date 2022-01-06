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

        self.function = {
            "help": self.help,
            "new_user": self.new_user,
            "new_pwd": self.new_pwd,
            "new_path": self.new_path,
            "download": self.download,
            "refresh": self.refresh,
            "encrypt": self.encrypt,
            "decrypt": self.decrypt,
            "new_encrypt_lvl": self.new_encryption_lvl
        }

        # TESTING
        # User login

        dm = displaymanager.DisplayManager(self)
        a = dm.get_usage_command("-c")
        b = dm.get_help_tree()

        dm.print_help("-c")

        tmp_user_name = "mneuhaus"
        tmp_user_password = "passwd123"
        tmp_password_hash = krypto_manager.hash_str(tmp_user_password)

        # CREATING USER
        #self.global_data_manager.create_user(tmp_user_name, tmp_password_hash)

        # CHECK LOGIN
        check = self.global_data_manager.check_user_hash(tmp_user_name, tmp_password_hash)
        print check
        self.user = None

        # PARSER return Dictionary with information about parameter and function
        args = "-u " + tmp_user_name + " -p " + tmp_user_password + " -d 0 "
        #args = "-u " + tmp_user_name + " -n S=s706:U=db74969:E=17eca6df980:C=17e2fef3180:P=185:A=mneuhaus:V=2:H=c0a3120a5067762e029985155fbdeb9a " + tmp_user_password
        par = param_loader_2.ArgumentParser(self, args)
        params = par.parser()
        self.username = params["username"]
        self.passwd = params["passwd"]
        print params
        #self.function[params["func"]](params)

        #self.user_web_auth()
        c = krypto_manager.CompressManager(self, self.username, self.passwd)
        c.compress()

        #dm = displaymanager.DisplayManager(self)
        #dm.print_help()

        # user_data_manager

    #####################
    # all start methods #
    #####################
    def help(self, params):
        """
        outputs help text on the terminal
        :param params: a dict containing all parsed arguments
        """
        self.displaymanager.print_help()

    def new_user(self, params):
        """
        Create a new user
        If usertoken equal to None, User is redirected to website
        :param params: a dict containing all parsed arguments
        """
        token = params["token"]
        if token == None:
            # TODO:
            pass
        self.user = self.global_data_manager.create_user(user_name=self.username, user_password=self.passwd, token=token)

    def new_pwd(self, params):
        """
        Change Password
        :param params: a dict containing all parsed arguments
        """
        new_pwd = params["new_pwd"]
        if not self.global_data_manager.is_user(self.username):
            return
        new_pwd_hash = krypto_manager.hash_str(new_pwd)
        self.global_data_manager.credentials.set(self.username, new_pwd_hash)
        self.global_data_manager.credentials.dump()

    def new_path(self, params):
        """
        change download path
        :param params: a dict containing all parsed arguments
        """
        new_path = params["new_path"]
        self.user = self.global_data_manager.get_user(self.username, self.passwd)
        self.user.set_custom_path(new_path)

    def new_encryption_lvl(self, params):
        """
        change encryption level
        :param params: a dict containing all parsed arguments
        """
        new_encrypt_lvl = params["new_encrypt_lvl"]
        self.user = self.global_data_manager.get_user(self.username, self.passwd)
        self.user.set_encryption_lvl(new_encrypt_lvl)

    def download(self, params):
        """
        Downloads all files from the accounts
        :param params: a dict containing all parsed arguments
        """
        self.user = self.global_data_manager.get_user(self.username, self.passwd)
        self.user.test_download()
        self.user.download_user_data()
        self.user.set_encryption_lvl(params["encryption_lvl"])

    def encrypt(self, params):
        """
        :return:
        """
        pass

    def decrypt(self, params):
        """
        :param params:
        :return:
        """
        pass

    def refresh(self, params):
        """
        :param params:
        :return:
        """
        pass

    ##########################################
    ##########################################

    def setup_logging(self, level=logging.INFO):
        """
        Used to make global configurations for the logger (format etc)
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
        """
        Returns logging object of Evernote object
        :return:
        """
        return self.logger

    def get_log_handler(self):
        """
        Returns logging handler to create own logger objects in different classes with global configuration
        :return:
        """
        return self.log_handler

    def create_logger(self, name):
        """
        Return a logger object with the name of the var
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
        execute_from_command_line(sys.argv[:1] + ["runserver"])


# main
if __name__ == "__main__":
    print(sys.argv[1:])

    e = Evernote(sys.argv[1:])
