
import json
import os
import copy
from helper import krypto_manager
import sys


# default encoding to utf-8 to process file_names
reload(sys)
sys.setdefaultencoding('UTF8')

class FileHandler:
    def __init__(self, file_name, path=None, create=False, exists_ok=False, *args, **params):
        # controller class
        self.controller = params.get("controller")

        self._file_name = file_name
        self._file_path = path

        # file ending
        self._mode = params.get("mode", "")

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
            else:
                if not os.path.exists(os.path.dirname(self._path)):
                    os.makedirs(os.path.dirname(self._path))

                with open(self._path, "w"):
                    pass

                if self.logger:
                    self.logger.warning("Created file: {}".format(self._path))

                return

        if self.logger:
            self.logger.info("Loading file: [}".format(self._path))

        # loading files depending on type
        if self._mode not in self.modes:
            if self.logger:
                self.logger.warn("loading default mode for: {} mode: {}".format(file_name, self._mode))
            self.load_default()
        else:
            self.modes[self._mode][0]()

    @property
    def path(self):
        return self._path

    @property
    def exists(self):
        return os.path.isfile(self._path)

    @property
    def file_hash(self):
        return krypto_manager.file_hash(self.path, hash_type="md5")

    def load_json(self):
        with open(self._path, "r") as file:
            self._file_data = json.load(file)
            
    def load_default(self):
        with open(self._path, "r" if not self._binary else "rb") as file:
            self._file_data = file.readlines()

    def get(self, key, *args):
        d = copy.deepcopy(self._file_data)
        return d.get(key, *args) if type(d) == dict else d

    def set(self, key, *args, **params):
        file_data = params.get("file_data", None) or args[0]
        if type(self._file_data) == dict:
            self._file_data[str(key)] = file_data
        else:
            self._file_data = file_data

    def addElement(self, key, e):
        if type(self._file_data) != dict:
            return
        self._file_data[str(key)].append(e)

    def dump(self):
        if self._mode in self.modes:
            self.modes[self._mode][1]()
        else:
            self.write_default()

    def write_json(self):
        with open(self._path, "w") as file:
            json.dump(self._file_data, file, ensure_ascii=False, indent=4)

    def write_default(self):
        with open(self._path, "w" if not self._binary else "wb") as file:
            file.writelines(self._file_data)

    def get_all(self):
        return copy.deepcopy(self._file_data)

    def set_all(self, file_data):
        self._file_data = file_data

    def write(self, text):
        if self._mode == "json":
            self.logger.warning("Tried to write plaintext into json")
        self._file_data += text

    def __str__(self):
        return "File: {}".format(self._path) if self.exists else False