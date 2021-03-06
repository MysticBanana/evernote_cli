import logging
import os
import sys

import enum
import oauth.auth
import codecs
from data import user, global_data_manager
from helper import krypto_manager, exception
from helper.interface import argument_parser, displaymanager


class Evernote:
    # todo dynamicly with __file__
    NAME = "evernote_cli.py"

    class ControllerError(exception.EvernoteException):
        class ErrorReason(enum.Enum):
            DEFAULT = 1

    def __init__(self, argv=None, **params):
        self._sandbox = True
        self._testing = True
        self._easter_egg = False
        self._version = "1.0.4"

        # change working dir to current dir
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.global_data_manager = global_data_manager.GlobalFileManager(self)

        self.log_level = params.get("log_level", logging.INFO)
        self.setup_logging(level=self.log_level)

        self.logger.info("Starting...")
        self.logger.info("Loaded .config.json")

        # setup logging for exceptions
        exception.EvernoteException.logger = self.get_logger()

        self.global_data_manager.setup_logging()
        self.global_data_manager.init_files()
        self._sandbox = self.global_data_manager.main_config.get("sandbox", True)
        self._testing = self.global_data_manager.main_config.get("testing", True)
        self._easter_egg = self.global_data_manager.main_config.get("cringe", False)

        exception.EvernoteException.testing = self._testing
        exception.EvernoteException.fun_mode = self._easter_egg

        self.display_manager = displaymanager.DisplayManager(self)

        self.function = {
            "help": self.help,
            "new_user": self.new_user,
            "new_pwd": self.new_pwd,
            "new_path": self.new_path,
            "download": self.download,
            "encrypt": self.encrypt,
            "decrypt": self.decrypt,
            "new_encrypt": self.new_encryption_lvl,
            "remove": self.remove,
            "error": self.error,
            "input_error": self.input_error,
            "version" : self.version
        }

        self.user = None

        # PARSER return Dictionary with information about parameter and function
        self.par = argument_parser.ArgumentParser(self, argv)
        self.par.parser()

        params = self.par.params

        try:
            if not params["func"] in ["version", "help", "error", "input_error"]:
                self.username = params["username"]
                self.password = params["password"]
                if not params["func"] == "new_user":
                    self.user = self.global_data_manager.get_user(self.username, self.password,
                                                                  force_mode=params.get("force", False),
                                                                  overwrite=params.get("overwrite", False))
            self.function[params["func"]](params)
        except exception.EvernoteException as e:
            self.logger.error("error while processing command\n%s" % e)
            raise self.ControllerError(e)
        except Exception as e:
            self.logger.error("error while processing command\n%s" % e)
            raise self.ControllerError(e)
        except KeyboardInterrupt:
            # todo bessere formulierung
            print "trying to close files"
            print "interrupt again for fast exit"
            self.logger.warning("KeyboardInterrupt by user, trying to close all files")
        finally:
            self.global_data_manager.close()
            if self.user is not None:
                self.user.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.user is not None:
            self.logger.warning("stopped program unexpected, trying to save all files")
            try:
                self.user.close()
            except Exception as e:
                self.logger.error("error while saving user files")
            finally:
                self.logger.info("stopped programm successfully")

    def setup_logging(self, level=logging.INFO):
        """
        Used to make global configurations for the logger (format etc)
        :param level:
        """
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')

        path = self.global_data_manager.get_path("log")
        fpath = path + "logfile.log"

        # check for exist
        if not os.path.isdir(path):
            os.makedirs(os.path.dirname(path))
            with open(fpath, "w"):
                pass

        # if logfile gets too big delete
        if os.path.isfile(fpath):
            if os.path.getsize(fpath) > 40000:
                with open(fpath, "w+"):
                    pass

        # setup log handler with correct format
        self.log_handler = logging.FileHandler(fpath)
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

    def user_web_auth(self):
        """
        Runs a local TCP server to handle the callback from evernote website
        :return: user access token to authenticate
        """
        self.auth = oauth.auth.Auth(controller=self, CONSUMER_KEY=self.global_data_manager.CONSUMER_KEY,
                                    CONSUMER_SECRET=self.global_data_manager.CONSUMER_SECRET, SANDBOX=self.sandbox,
                                    logger=self.create_logger("OAuth"))
        return self.auth.access_token

    @property
    def sandbox(self):
        return self._sandbox

    @sandbox.setter
    def sandbox(self, value):
        # not not is faster than bool()
        value = not not value

        if self.global_data_manager:
            self.global_data_manager.main_config.set("sandbox", value).dump()
            self._sandbox = value

            self.logger.info("sandbox set to %s" % value)

    @property
    def max_encryption_level(self):
        # used for validation in user input
        return 2 ** len(user.User.EncryptionLevel) - 1


    #####################
    # all start methods #
    #####################

    def help(self, params):
        """
        outputs help text on the terminal
        :param params: a dict containing all parsed arguments
        """

        p = params["command"]
        self.display_manager.print_help(p)

    def new_user(self, params):
        """
        Create a new user
        If usertoken equal to None, User is redirected to website
        :param params: a dict containing all parsed arguments
        """
        token = params["token"]


        if token == -1:
            return
        elif not token:
            token = self.user_web_auth()
            if not token:
                print "Bad request syntax: Try again!"
                return
        self.user = self.global_data_manager.create_user(user_name=self.username, user_password=self.password, token=token)

    def new_pwd(self, params):
        """
        Change Password
        :param params: a dict containing all parsed arguments
        """
        new_pwd = params["new_password"]
        if not self.global_data_manager.is_user(self.username):
            return
        new_pwd_hash = krypto_manager.hash_str(new_pwd)
        self.global_data_manager._credentials.set(self.username, new_pwd_hash)
        self.global_data_manager._credentials.dump()
        self.user.km = krypto_manager.CryptoManager(key=new_pwd, salt="user", logger=self.create_logger("Krypto"))

    def new_path(self, params):
        """
        change download path
        :param params: a dict containing all parsed arguments
        """
        new_path = params["new_path"]
        # self.user = self.global_data_manager.get_user(self.username, self.passwd)
        self.user.file_path = new_path

        # would try to encrypt a empty dir and raise error
        self.user.encryption_level = 0

    def new_encryption_lvl(self, params):
        """
        change encryption level
        :param params: a dict containing all parsed arguments
        """
        new_encrypt_lvl = params["new_encrypt_lvl"]
        # self.user = self.global_data_manager.get_user(self.username, self.passwd)
        self.user.encryption_level = new_encrypt_lvl

    def download(self, params):
        """
        Downloads all files from the accounts
        :param params: a dict containing all parsed arguments
        """
        # self.user = self.global_data_manager.get_user(self.username, self.passwd)

        # todo set encryption level before and add "force" too here need your help @tom
        self.user.test_download()
        self.user.download_user_data()
        el = params.get("encryption_lvl", None)
        if el:
            self.user.encryption_level = el

    def encrypt(self, params):
        """
        :return:
        """
        self.user.encryption_level = params.get("encryption_lvl", 3)

    def decrypt(self, params):
        """
        :param params:
        :return:
        """
        self.user.encryption_level = 0

    def remove(self, params):
        self.global_data_manager.remove_user(params["username"])
        self.user = None

    def error(self, params):
        print params["err_types"][0]

    def input_error(self, params):
        print params["err_types"][0]


    def version(self, params):
        print self._version

# https://code.activestate.com/recipes/572200/
def win32_unicode_argv():
    """Uses shell32.GetCommandLineArgvW to get sys.argv as a list of Unicode
    strings.

    Versions 2.x of Python don't support Unicode in sys.argv on
    Windows, with the underlying Windows API instead replacing multi-byte
    characters with '?'.

    https://code.activestate.com/recipes/572200/
    """

    from ctypes import POINTER, byref, cdll, c_int, windll
    from ctypes.wintypes import LPCWSTR, LPWSTR

    GetCommandLineW = cdll.kernel32.GetCommandLineW
    GetCommandLineW.argtypes = []
    GetCommandLineW.restype = LPCWSTR

    CommandLineToArgvW = windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.argtypes = [LPCWSTR, POINTER(c_int)]
    CommandLineToArgvW.restype = POINTER(LPWSTR)

    cmd = GetCommandLineW()
    argc = c_int(0)
    argv = CommandLineToArgvW(cmd, byref(argc))
    if argc.value > 0:
        # Remove Python executable and commands if present
        start = argc.value - len(sys.argv)
        return [argv[i] for i in
                xrange(start, argc.value)]

# main
if __name__ == "__main__":

    # check if running on windows because argv is bytestring and needs to be converted
    if sys.platform == "win32":
        sys.argv = win32_unicode_argv()
        params = [unicode(i) for i in sys.argv[1:]]
    else:
        params = sys.argv[1:]

    # e = Evernote(
    #       "-u {user_name} -p {password} -c -e 0".format(user_name=tmp_user_name, password=tmp_user_password, token=token).split(" "))
    # e = Evernote("-h -p".format(user_name=tmp_user_name, password=tmp_user_password).split(" "))
    e = Evernote(params)
