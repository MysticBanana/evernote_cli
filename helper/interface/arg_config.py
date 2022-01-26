import copy

class Command(dict):
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, *args):
        return self.__dict__.get(key, *args)

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))


class ParameterStructure:
    # nested Commands
    parameter = None

    # all optional Parameter, where no error gets raised if not in right context
    optionals = []

    # default usage string if too complex and hard coding is easier to read for user
    default_usage = ""

    optional_str = "[{}]"
    user_input_str = "<{}>"
    exclusive_str = "({})"
    or_str = " | "

    app_name = "evernote_cli.py"

    def __init__(self, *args, **kwargs):
        parameter = kwargs.get("parameter", Command())
        self.parameter = self.init_commands(parameter)

    def init_commands(self, command_list):
        for k, v in command_list.items():
            if isinstance(v, dict):
                command_list[k] = self.create_command(v)

        return command_list

    def create_command(self, command):
        if type(command) != dict:
            return

        new_command = Command()
        opt_str = command.get("opt_str", None)
        if not opt_str:
            return

        new_command["opt_str"] = opt_str
        new_command["name"] = command.get("name", "default name")

        # if command is a sub command and is / is not needed for a command
        new_command["optional"] = command.get("optional", True)

        # gets displayed on a normal help menu request
        new_command["help"] = command.get("help", "default help text")

        # gets displayed when user asked for specific help (longer description of command)
        new_command["long_help"] = command.get("long_help", "longer default description")

        new_command["func"] = command.get("func", None)  # maybe func reference idk
        new_command["func_name"] = command.get("func_name", "idk man thats useless")

        # options that are required for this command (also optional)
        # as a {param: True} while true stands for not optional
        new_command["requires"] = command.get("requires", {})
        new_command["subcommand"] = command.get("subcommand", [])

        if len(new_command["subcommand"]) != 0:
            for k, v in new_command["subcommand"].items():
                if isinstance(v, dict):
                    new_command["subcommand"][k] = self.create_command(v)

        return new_command

    def get_command(self, command_name):
        return self.dict_search(self.parameter, command_name)

    def add_subcommand(self, command_name, new_command):
        # self.get_command(command_name)["subcommand"].append(new_command)
        self.get_command(command_name)["subcommand"][new_command["name"]] = new_command

    def dict_search(self, d, search, path=False):
        # path is if path to the nested dict is needed
        # search can be a dict or string

        for k, v in d.items():
            if isinstance(v, dict):
                if isinstance(search, dict) and search == v:
                    return v, [k] if path else v
                elif v.get("name", "") == search or search in v.get("opt_str", ""):
                    return v, [k] if path else v
                else:
                    if len(v.get("subcommand", [])) == 0:
                        continue
                    _v = self.dict_search(v["subcommand"], search, path=path)
                    if not _v:
                        continue

                    if path:
                        p = _v[1]
                        _v = _v[0]
                        p.append(k)
                        return _v, p
                    return _v

    def get_usage(self, command=None):
        if command is None:
            return self.default_usage

        # if not isinstance(command, dict):
        #     return

        usage = "$%s " % self.app_name

        c, path = self.dict_search(self.parameter, command, path=True)
        path.reverse()

        dict_path = copy.deepcopy(self.parameter)
        for cmd in path:
            if len(dict_path) == 0:
                break

            c = dict_path[cmd]


            u = c.get("opt_str")[0]
            if len(c.get("requires", [])) != 0:
                # get optional and none optional parameters now
                n_opt = c["requires"].get("none_opt", [])
                if len(n_opt) == 1:
                    u += " {}".format(self.make_user_input(n_opt[0]))
                elif len(n_opt) > 1:
                    u += " " + ", ".join(self.make_user_input(n_opt))

                opt = c["requires"].get("opt", [])
                if len(opt) != 0:
                    # oopt = [self.make_optional(self.make_user_input(i) if type(i) == str else i[0]) for i in opt]
                    for i in opt:
                        if type(i) == str:
                            oopt = self.make_user_input(i)
                        else:
                            oopt = i[0]
                            if type(i[1]) == str and i[1][0] == "-":
                                pass
                            else:
                                oopt = self.make_user_input(oopt)

                        u += " " + self.make_optional(oopt)

            usage += u + " "
            dict_path = dict_path[cmd]["subcommand"]

        return usage




    def make_exclusive(self, *args):
        return self.exclusive_str.format(self.or_str.join(args))

    def make_optional(self, *args):
        return self.optional_str.format(self.or_str.join(args))

    def make_user_input(self, *args):
        # todo make decorator of
        args = [i[0] if type(i) != str else i for i in args]
        return self.user_input_str.format(self.or_str.join(args))


# should change subcommand to list
commands = {
    "version":
        {
            "name": "version",
            "opt_str": ["-v", "--version"],
            "help": "shows version of the program",
            "long_help": "",
            "func_name": "version",
        },
    "help":
        {
            "name": "help",
            "opt_str": ["-h", "--help"],
            "help": "shows this menu or help text for command",
            "long_help": "",
            "func_name": "help",
            "requires": {
                "opt": ["command"],
            }
        },
    "user":
        {
            "name": "user",
            "opt_str": ["-u", "--user"],
            "help": "used in combination with --new or --passwd",
            "long_help": "",
            "func_name": None,
            "requires": {
                "none_opt": ["username"],
            },
            "subcommand": {
                "new_user":
                    {
                        "name": "new_user",
                        "opt_str": ["-n", "--new"],
                        "help": "create new user",
                        "long_help": "",
                        "func_name": "new_user",
                        "requires": {
                            "none_opt": ["password"],
                            "opt": [("token", str)]
                        }
                    },
                "passwd":
                    {
                        "name": "passwd",
                        "opt_str": ["-p", "--passwd"],
                        "help": "input your stupid password after",
                        "long_help": "",
                        "requires": {
                            "none_opt": ["password"],
                        },
                        "subcommand":
                            {
                                "change":
                                    {
                                        "name": "change",
                                        "opt_str": ["-c", "--change"],
                                        "help": "change stuff ",
                                        "long_help": "",
                                        "subcommand":
                                            {
                                                "new_pwd":
                                                    {
                                                        "name": "new_pwd",
                                                        "opt_str": ["-p", "--passwd"],
                                                        "help": "change password",
                                                        "long_help": "",
                                                        "func_name": "new_pwd",
                                                        "requires": {
                                                            "none_opt": ["new_password"],
                                                            "opt": [("force", "-f")]
                                                        }
                                                    },
                                                "new_path":
                                                    {
                                                        "name": "new_path",
                                                        "opt_str": ["-d", "--downloadpath"],
                                                        "help": "change download path",
                                                        "long_help": "",
                                                        "func_name": "new_path",
                                                        "requires": {
                                                            "none_opt": ["new_path"],
                                                            "opt": [("force", "-f")]
                                                        }
                                                    },
                                                "new_encrypt":
                                                    {
                                                        "name": "new_encrypt",
                                                        "opt_str": ["-e", "--encrypt_files"],
                                                        "help": "change download encryption level",
                                                        "long_help": "",
                                                        "func_name": "new_encrypt",
                                                        "requires": {
                                                            "none_opt": [("new_encrypt_lvl", int)],
                                                            "opt": [("force", "-f")]
                                                        }
                                                    },
                                            }
                                    },
                                "download":
                                    {
                                        "name": "download",
                                        "opt_str": ["-d", "--download"],
                                        "help": "download all files",
                                        "long_help": "",
                                        "func_name": "download",
                                        "requires": {
                                            "opt": [("force", "-f"), ("overwrite", "-o"), "encryption_lvl"]
                                        }
                                    },
                                "encrypt":
                                    {
                                        "name": "encrypt",
                                        "opt_str": ["-e", "--encrypt"],
                                        "help": "encrypting your files",
                                        "long_help": "",
                                        "func_name": "encrypt",
                                        "requires": {
                                            "opt": [("encryption_lvl", int)]
                                        }
                                    },
                                "decrypt":
                                    {
                                        "name": "decrypt",
                                        "opt_str": ["-de", "--decrypt"],
                                        "help": "decrypting your files",
                                        "long_help": "",
                                        "func_name": "decrypt",
                                        "requires": {
                                            "opt": [("encryption_lvl", int)]
                                        }
                                    },
                                "refresh":
                                    {
                                        "name": "refresh",
                                        "opt_str": ["-r", "--refresh"],
                                        "help": "synchronize your files with the cloud",
                                        "long_help": "",
                                        "func_name": "refresh"
                                    },
                                "remove":
                                    {
                                        "name": "remove",
                                        "opt_str": ["-rm", "--remove"],
                                        "help": "remove user",
                                        "long_help": "",
                                        "func_name": "remove"
                                    }
                            }
                    }
            }
        }
}

if __name__ == "__main__":
    parameter_structure = ParameterStructure(parameter=commands)

    # print parameter_structure.parameter
    # print parameter_structure.get_usage(parameter_structure.get_command("user"))
    print parameter_structure.get_usage("new_encrypt")






"""
> sum -d -e to -de?
> optional arguments possible for all commands, just getting irgnored
> description/Category of a command

Commands
    version
    help
    remove user
    user
    new user
    
    Options
        - p
        ...
"""
