import enum
# import param_loader_2

arguments = {
    "user":
        {
            "subparser": True,
            "help": "user -h",
            "default": True,
            # pos_arg
            "username":
                {
                    "subparser": False,
                    "opt_str": ["username"],
                    "action": None,
                    "nargs": 1,
                    "const": None,
                    "default": None,
                    "type": str,
                    "choices": None,
                    "help": "Your username for Evernote",
                    "metavar": "USERNAME"
                },
            # subparser
            "token":
                {
                    "subparser": True,
                    "help": "token -h",
                    "default": True,
                    # pos_arg
                    "token":
                        {
                            "subparser": False,
                            "opt_str": ["token"],
                            "action": None,
                            "nargs": 1,
                            "const": None,
                            "default": None,
                            "type": str,
                            "choices": None,
                            "help": "Your usertoken for Evernote",
                            "metavar": "TOKEN"
                        },
                    "passwd":
                        {
                            "subparser": False,
                            "opt_str": ["passwd"],
                            "action": None,
                            "nargs": 1,
                            "const": None,
                            "default": None,
                            "type": str,
                            "choices": None,
                            "help": "Your self chosen password for the Evernote CLI",
                            "metavar": "PASSWD"
                        },
                },
            "passwd":
                {
                    "subparser": True,
                    "help": "passwd -h",
                    "default": True,
                    # pos_arg
                    "passwd":
                        {
                            "subparser": False,
                            "opt_str": ["passwd"],
                            "action": None,
                            "nargs": 1,
                            "const": None,
                            "default": "PASSWORD",
                            "type": str,
                            "choices": None,
                            "help": "Password for the evernote-CLI",
                            "metavar": "PASSWD"
                        },
                    # opt_arg
                    "find":
                        {
                            "subparser": False,
                            "opt_str": ["-f", "--find"],
                            "action": None,
                            "nargs": 1,
                            "const": None,
                            "default": None,
                            "type": str,
                            "choices": None,
                            "required": False,
                            "help": "Finding the downloadpath for note, notebook or tag",
                            "metavar": "TAG | NOTENAME | NOTEBOOKNAME",
                            "dest": "find"
                        },
                    "delete":
                        {
                            "subparser": False,
                            "opt_str": ["-d", "--delete"],
                            "action": None,
                            "nargs": 1,
                            "const": None,
                            "default": None,
                            "type": str,
                            "choices": None,
                            "required": False,
                            "help": "Delete note, notebook (or user)",
                            "metavar": "NOTENAME | NOTEBOOKNAME | (USERNAME)",
                            "dest": "delete"
                        },
                    "sync":
                        {
                            "subparser": False,
                            "opt_str": ["-s", "--sync"],
                            "action": None,
                            "nargs": 1,
                            "const": True,
                            "default": True,
                            "type": None,
                            "choices": None,
                            "required": False,
                            "help": "Sync with the Cloud",
                            "metavar": "",
                            "dest": None
                        },
                    # subparser
                    "show":
                        {
                            "subparser": True,
                            "help": "show -h",
                            "default": True,
                            # opt_arg
                            "file":
                                {
                                    "subparser": False,
                                    "opt_str": ["-f", "--file"],
                                    "action": None,
                                    "nargs": 1,
                                    "const": None,
                                    "default": None,
                                    "type": str,
                                    "choices": None,
                                    "required": False,
                                    "help": "show files",
                                    "metavar": "PATH | NOTENAME | NOTEBOOKNAME",
                                    "dest": "FILE"
                                },
                            "user":
                                {
                                    "subparser": False,
                                    "opt_str": ["-u", "--user"],
                                    "action": None,
                                    "nargs": 1,
                                    "const": None,
                                    "default": None,
                                    "type": str,
                                    "choices": None,
                                    "required": False,
                                    "help": "show userdata",
                                    "metavar": "USERNAME",
                                    "dest": "user"
                                },
                            "path":
                                {
                                    "subparser": False,
                                    "opt_str": ["-p", "--path"],
                                    "action": None,
                                    "nargs": 1,
                                    "const": None,
                                    "default": None,
                                    "type": str,
                                    "choices": None,
                                    "required": False,
                                    "help": "show path of NOTE or NOTEBOOK",
                                    "metavar": "NOTENAME | NOTEBOOKNAME",
                                    "dest": "path"
                                }
                        },
                    "change":
                        {
                            "subparser": True,
                            "help": "change -h",
                            "default": True,
                            # pos_arg
                            "new_pwd_path":
                                {
                                    "subparser": False,
                                    "opt_str": ["new_pwd_path"],
                                    "action": None,
                                    "nargs": 1,
                                    "const": None,
                                    "default": None,
                                    "type": str,
                                    "choices": None,
                                    "help": "new path or password",
                                    "metavar": "NEW_PWD_PATH"
                                },
                            # opt_arg
                            "passwd":
                                {
                                    "subparser": False,
                                    "opt_str": ["-p", "--passwd"],
                                    "action": None,
                                    "nargs": 1,
                                    "const": None,
                                    "default": None,
                                    "type": str,
                                    "choices": None,
                                    "required": False,
                                    "help": "Current Password",
                                    "metavar": "OLD_PASSWD",
                                    "dest": "old_pwd"
                                },
                            "downloadpath":
                                {
                                    "subparser": False,
                                    "opt_str": ["-d", "--downloadpath"],
                                    "action": None,
                                    "nargs": 1,
                                    "const": None,
                                    "default": None,
                                    "type": str,
                                    "choices": None,
                                    "required": False,
                                    "help": "Old downloadpath",
                                    "metavar": "OLDPATH",
                                    "dest": "old_path"
                                },
                        },
                    "download":
                        {
                            "subparser": True,
                            "help": "download -h",
                            "default": True,
                            # opt_arg
                            "all":
                                {
                                    "subparser": False,
                                    "opt_str": ["-a", "--all"],
                                    "action": None,
                                    "nargs": 1,
                                    "const": True,
                                    "default": True,
                                    "type": None,
                                    "choices": None,
                                    "required": False,
                                    "help": "download all",
                                    "metavar": "",
                                    "dest": None
                                },
                        }
                }

        }
}

class DisplayManager:
    def __init__(self, controller):
        self.controller = controller
        self.logger = controller.create_logger("Display")

        self.tab_size = "   "

    def default_display(self, display_text):
        self.logger.debug(display_text)

    def default_error(self, reason):
        self.logger.error(reason)
        raise EvernoteException (reason)

    def display_dict(self, data):
        # dictionary displayed: "-u --user              help text zu -u"
        pass

    def get_dict(self, arg="-h"):
        self.help_dict = param_loader_2.ArgumentParser.args_dict

    def print_help(self, ret_dict=None, tab_counter=0):
        ret_dict = ret_dict if ret_dict else arguments

        for k, v in ret_dict.items():

            if type(v) == dict:
                if "opt_str" in v:
                    string = "{tabs}{opt_str} <{metavar}> {helptext}".format(opt_str=v["opt_str"],
                                                                             metavar=v["metavar"], helptext=v["help"],
                                                                             tabs=(self.tab_size * tab_counter))
                    print(string)
                else:
                    self.print_help(v, tab_counter + 1)

class EvernoteException(BaseException):
    class Exceptions(enum.Enum):
        pass
        token = {
            "subparser": False,
            "opt_str": ["token"],
            "action": None,
            "nargs": 1,
            "const": None,
            "default": None,
            "type": str,
            "choices": None,
            "help": "Your usertoken for Evernote",
            "metavar": "TOKEN"
        }
        string = "{} <{}> {}".format(token["opt_str"], token["metavar"], token["help"])

def _print_help(ret_dict=None, tab_counter=0):
    ret_dict = ret_dict if ret_dict else arguments
    tab_size = "   "

    for k, v in ret_dict.items():

        if type(v) == dict:
            if "opt_str" in v:
                string = "{tabs}{opt_str} <{metavar}> {helptext}".format(opt_str=v["opt_str"],
                                                                          metavar=v["metavar"], helptext=v["help"],
                                                                            tabs=(tab_size*(tab_counter-1)))
                print(string)
            else:
                _print_help(v, tab_counter+1)

if __name__ == "__main__":
    _print_help()