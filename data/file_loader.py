import json
import os
import copy
import sys
from shutil import copyfile

class Config:
    def __init__(self, config_name, path="", create=False, **params):
        # for encoding in files?
        reload(sys)
        sys.setdefaultencoding('utf-8')

        self.main_class = params.get("main_class")
        self.config_name = config_name
        self.mode = params.get("mode", "json")
        self.path = path + self.config_name + "." + self.mode

        if params.get("logging", None):
            self.logger = self.main_class.create_logger("FileLoader")
        else:
            self.logger = None
        
        self.modes = {
            "json": self.load_json
        }

        if not os.path.exists(self.path):
            if not create:
                self.main_class.exit_error("File does not exist: " + str(self.path))
                return
            open(self.path, "w").close()

        if self.mode not in self.modes:
            if self.logger: self.logger.warn("loading default mode for: " + str(config_name) + " mode: " + str(self.mode))
            self.load_default()

        if self.logger: self.logger.info("loading file: " + str(config_name))
        self.modes[self.mode]()

    def load_json(self):
        with open(self.path, "r") as file:
            self.file_data = json.load(file)
            
    def load_default(self):
        pass # self.set("asf", file_data="{}")

    def get(self, key, *args):
        d = copy.deepcopy(self.file_data)
        return d.get(key, *args)

    def set(self, key, **params):
        file_data = params.get("file_data")
        self.file_data[str(key)] = file_data

    def addElement(self, key, e):
        self.file_data[str(key)].append(e)

    def dump(self):
        with open(self.path, "w") as file:
            json.dump(self.file_data, file, ensure_ascii=False, indent=4)

    def getAll(self):
        d = copy.deepcopy(self.file_data)
        return d

    def setAll(self, file_data):
        self.file_data = file_data