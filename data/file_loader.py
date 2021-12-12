import json
import os
import copy
from helper import krypto_manager


class FileHandler:
    def __init__(self, file_name, path=None, create=False, *args, **params):
        # controller class
        self.controller = params.get("controller")

        self._file_name = file_name
        self._file_path = path

        # file ending
        self._mode = self.mode = params.get("mode", "json")

        # full path to open
        self._path = "{}{}{}".format(path if path is not None else "", file_name, ".{}".format(self._mode) if self._mode is not None else "")

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

        if self.logger:
            self.logger.info("Loading file: [}".format(self._path))

        # loading files depending on type
        if self.mode not in self.modes:
            if self.logger:
                self.logger.warn("loading default mode for: {} mode: {}".format(file_name, self._mode))
            self.load_default()
        else:
            self.modes[self.mode][0]()

    @property
    def exists(self):
        return os.path.isfile(self._path)

    @property
    def file_hash(self):
        return krypto_manager.file_hash(self._path)

    def load_json(self):
        with open(self._path, "r") as file:
            self._file_data = json.load(file)
            
    def load_default(self):
        with open(self._path, "r") as file:
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
        if self.mode in self.modes:
            self.modes[self.mode][1]()
        else:
            self.write_default()

    def write_json(self):
        with open(self._path, "w") as file:
            json.dump(self._file_data, file, ensure_ascii=False, indent=4)

    def write_default(self):
        with open(self._path, "w") as file:
            file.writelines(self._file_data)

    def get_all(self):
        return copy.deepcopy(self._file_data)

    def set_all(self, file_data):
        self._file_data = file_data

    def write(self, text):
        if self.mode == "json":
            self.logger.warning("Tried to write plaintext into json")
        self._file_data += text

    def __str__(self):
        return "File: {}".format(self._path) if self.exists else False