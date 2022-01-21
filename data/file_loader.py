# encoding: utf-8


import json
import os
import copy
from helper import krypto_manager, exception
import sys
import enum


# default encoding to utf-8 to process file_names
reload(sys)
sys.setdefaultencoding('UTF8')

class FileHandler:
    class FileHandlerException(exception.EvernoteException):
        class ErrorReason(enum.Enum):
            DEFAULT = 1
            FILE_NO_PERMISSION = 3
            WRONG_FILE_FORMAT = 4
            ERROR_WRITING_IN_FILE = 5
            ERROR_READING_FILE = 6
            ERROR_CREATING_PATH = 7

    def __init__(self, file_name, path=None, create=False, exists_ok=False, *args, **params):
        """
        Opening file and saving content depending on opening mode
         - store json data in dict
         - stores not defined files in plain string

        :rtype: object
        """
        # todo async write to file
        # controller class
        self.controller = params.get("controller")

        self._file_name = file_name
        self._file_path = path

        # file ending
        self._mode = params.get("mode", "")
        self._overwrite = params.get("overwrite", False)

        # open in binary mode
        self._binary = params.get("binary", False)

        # full path to open
        self._path = "{}{}{}".format(self._file_path if self._file_path is not None else "", file_name, ".{}".format(self._mode) if self._mode is not None else "").decode("utf-8")

        # var where data is stored
        self._file_data = None

        # setup logging is possible
        if params.get("logging", None):
            self.logger = self.controller.create_logger("FileLoader")
        else:
            self.logger = None

        self.modes = {
            "json": [self.load_json, self.write_json]
        }

        if not self.exists:
            if not create:
                if self.logger:
                    self.logger.warning("File: {} does not exists".format(self._path))
                raise self.FileHandlerException(self.FileHandlerException.ErrorReason.FILE_DOES_NOT_EXIST)
            else:
                if not os.path.exists(os.path.dirname(self._path)):
                    try:
                        os.makedirs(os.path.dirname(self._path))
                    except Exception:
                        self.FileHandlerException(self.FileHandlerException.ErrorReason.ERROR_CREATING_PATH,
                                                  "path %s" % self._path)

                with open(self._path, "w"):
                    pass

                if self.logger:
                    self.logger.warning("Created file: {}".format(self._path))

                return

        if self._overwrite:
            with open(self._path, "w"):
                pass
            return

        if self.logger:
            self.logger.info("Loading file: {}".format(self._path))

        # loading files depending on type
        try:
            if self._mode not in self.modes:
                if self.logger:
                    self.logger.warn("loading default mode for: {} mode: {}".format(file_name, self._mode))
                self.load_default()
            else:
                self.modes[self._mode][0]()

        except Exception as e:
            raise self.FileHandlerException(self.FileHandlerException.ErrorReason.ERROR_READING_FILE,
                                            "File: {} \nMode: {} \nStacktrace: {}".format(self._path, self._mode, e))

    @property
    def path(self):
        """
        getter for the path
        """
        return self._path

    @property
    def exists(self):
        """
        is True if the path is a file
        """
        return os.path.isfile(self._path)

    @property
    def file_hash(self):
        return krypto_manager.file_hash(self.path, hash_type="md5")

    def load_json(self):
        """
        stores json data in dict
        """
        with open(self._path, "r") as file:
            try:
                self._file_data = json.load(file)
            except Exception as e:
                raise self.FileHandlerException(self.FileHandlerException.ErrorReason.WRONG_FILE_FORMAT,
                                                "Error parsing the file %s" % self._path)
            
    def load_default(self):
        """
        stores file content as string in self._file_data
        """
        with open(self._path, "r" if not self._binary else "rb") as file:
            self._file_data = file.readlines()

    def get(self, key, *args):
        """
        returns value of file_data[key] or equivalent of get_all for default_mode
        :rtype: object
        """
        d = copy.deepcopy(self._file_data)
        return d.get(key, *args) if type(d) == dict else d

    def set(self, key, *args, **params):
        """
        set value of file_data[key] or equivalent of set_all for default_mode
        """
        file_data = params.get("file_data", None) or args[0]
        if type(self._file_data) == dict:
            self._file_data[str(key)] = file_data
        else:
            self._file_data = file_data

        return self

    def add_element(self, key, e):
        """
        adding an element to a list in the dictionary
        :param key: key of the dict
        :param e: data
        """
        if type(self._file_data) != dict:
            return
        self._file_data[str(key)].append(e)

        return self

    def dump(self):
        """
        Calls methode for saving data
        """
        try:
            if self._mode in self.modes:
                self.modes[self._mode][1]()
            else:
                self.write_default()
        except Exception as e:
            raise self.FileHandlerException(self.FileHandlerException.ErrorReason.ERROR_WRITING_IN_FILE,
                                            "File: {} \n Mode: {}".format(self._path, self._mode))

    def write_json(self):
        """
        saving data into json
        """
        with open(self._path, "w") as file:
            try:
                json.dump(self._file_data, file, ensure_ascii=False, indent=4)
            except Exception as e:
                raise self.FileHandlerException(self.FileHandlerException.ErrorReason.WRONG_FILE_FORMAT,
                                                "Error parsing the file %s" % self._path)


    def write_default(self):
        """
        saving data as plaintext
        """
        with open(self._path, "w" if not self._binary else "wb") as file:
            file.writelines(self._file_data)

    def get_all(self):
        """
        returns all data
        """
        return copy.deepcopy(self._file_data)

    def set_all(self, file_data):
        """
        set complete data to file_data (replace)
        :param file_data: new file_data
        """
        self._file_data = file_data

        return self

    def write(self, text):
        """
        appending text string to file_data, no check right file mode (not saving)
        :param text: string
        """
        if self._mode == "json":
            self.logger.warning("Tried to write plaintext into json")
        self._file_data += text

        return self

    def __str__(self):
        return "File: {}".format(self._path) if self.exists else False

    def __del__(self):
        self.dump()