import copy
from helper import decorator


class Command(dict):
    """
    Custom dictionary for custom access
    """
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

    def __cmp__(self, other):
        return self.__dict__ == other

    # if other is not a Command
    @decorator.exception_handler(stop=False)
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))


class ParameterStructure:
    """Stores the dictionary of all available parameter.
    Used for custom output for example usage strings or help menus"""

    # nested Commands
    parameter = None

    # all optional Parameter, where no error gets raised if not in right context
    optionals = ["force", "overwrite"]

    # default usage string if too complex and hard coding is easier to read for user
    default_usage = "[-h] [-u <username> (-n <password> [<token>] | -p <password>) --command]"
    default_description = "A console based client for the Evernote API"
    default_finish_str = "For complete documentation visit: <https://github.com/MysticBanana/evernote_cli>"

    # string prototypes for formating
    optional_str = "[{}]"
    user_input_str = "<{}>"
    exclusive_str = "({})"
    or_str = " | "

    # to display a help menu line in right syntax
    # don't change if you are not changing the depth of all commands
    help_line = "{space}{0:<{max_space}} {1:<2{max_space}}{2:<20}"
    max_space = 5

    # app name should be set from Controller
    app_name = "evernote_cli.py"

    def __init__(self, *args, **kwargs):
        """
        Can used to initialise the dictionary. If no parameter given commands have to get added via add_command
        """
        parameter = kwargs.get("parameter", Command())
        self.parameter = self.init_commands(parameter)

    def init_commands(self, command_list):
        """
        Recursive function to convert all commands in command_list in proper format
        :param command_list: command dictionary
        :return: initialised command dictionary
        """
        for k, v in command_list.items():
            if isinstance(v, dict):
                command_list[k] = self.create_command(v)
        return command_list

    def create_command(self, command):
        """
        Convert a Dictionary in "Command" and adds default values
        :param command: dict with all necessary values
        :return: "Command"
        """
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

        # for comments/notes for using this command
        new_command["note"] = command.get("note", "")

        new_command["func"] = command.get("func", None)  # maybe func reference idk
        new_command["func_name"] = command.get("func_name", "idk man thats useless")

        # options that are required for this command (also optional)
        # as a {param: True} while true stands for not optional
        new_command["requires"] = command.get("requires", {})
        new_command["subcommand"] = command.get("subcommand", {})

        if len(new_command["subcommand"]) != 0:
            for k, v in new_command["subcommand"].items():
                if isinstance(v, dict):
                    new_command["subcommand"][k] = self.create_command(v)

        return new_command

    def get_command(self, command_name):
        """
        Getter for Commands in the parameter dictionary
        :param command_name: can be the "name", the opt_str ("-u" or "--user") or Command
        :return: "Command"
        """
        return self.dict_search(self.parameter, command_name)

    def get_command_from_chain(self, *command_chain):
        """
        Same as get_command but also accept the user input string and returns the last possible command
        example: "-u username -p password -d" will return the "Command" of download (-d)
        :param command_chain: user input string split to list
        :return: "Command"
        """
        if len(command_chain) == 0:
            return

        if isinstance(command_chain[0], list):
            command_chain = command_chain[0]

        command = None
        for i in command_chain:
            if i[0] != "-":
                continue
            if not command:
                command = self.get_command(
                    command_chain[0])  # maybe replace with just trying to get command in base commands
                continue
            else:
                for k, v in command["subcommand"].items():
                    if i in v.get("opt_str", ""):
                        command = v
                        continue
                continue
        return command

    def add_subcommand(self, command, new_command):
        """
        Adds a subcommand "Command" in the dict "subcommand" in command
        :param command: the "Command" where to add the subcommand
        :param new_command: gets added to command
        """
        self.get_command(command)["subcommand"][new_command["name"]] = new_command

    # path is if path to the nested dict is needed
    # search can be a dict or string
    def dict_search(self, d, search, path=False):
        """
        Recursive look up for a command. Available to return the key-path too (list of all keys needed to reach the command
        :param d: dictionary where to look in
        :param search: name, opt_str or command to look for
        :param path: True or False if the path is needed
        :return: first "Command"
        """
        for k, v in d.items():
            if isinstance(v, dict):
                if isinstance(search, dict) and search == v:
                    return (v, [k]) if path else v
                elif v.get("name", "") == search or search in v.get("opt_str", ""):
                    return (v, [k]) if path else v
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

    # str
    def get_usage(self, command=None):
        """
        Convert all parameters needed and shows all available optional and none optional parameters
        :param command: command to print usage string for
        :return: usage string
        """
        if command is None:
            return "$%s %s " % (self.app_name, self.default_usage)

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

    # str
    def get_help_tree(self, command=None):
        """
        Converts all parameter in a easy readable string(opt_str + short help text)
        :param command: command to print usage string for
        :return: help tree string
        """
        def dict_parse(d, rec_counter=0):
            """
            adds all command strings in a list
            """
            # counts depth of dict
            rec_counter = rec_counter

            # lines of command strings
            lines = []

            if isinstance(d, dict):
                for k, v in d.items():
                    if isinstance(v, dict):
                        command_text = self.help_line.format(v["opt_str"][0], v["opt_str"][1], v["help"],
                                                             max_space=self.max_space - rec_counter,
                                                             space=rec_counter * "  ")

                        lines.append(command_text)

                        if len(v["subcommand"]) != 0:
                            # list from sub commands
                            sub_lines = dict_parse(v["subcommand"], rec_counter + 1)
                            for i in sub_lines:
                                lines.append(i)
                            # return list(sub_lines)
                return list(lines)

        # parameter tree, deepcopy to avoid changes
        tree = copy.deepcopy(self.parameter)

        if command is not None:
            command = self.dict_search(tree, command)
            tree = command.get("subcommand", None)

            line_list = dict_parse(tree, 1)
            command_text = self.help_line.format(command["opt_str"][0], command["opt_str"][1], command["help"],
                                                 max_space=self.max_space, space="")

            line_list.insert(0, command_text)

        else:
            line_list = dict_parse(tree)

        lines = ""
        if not line_list:
            # not a command
            return

        for i in line_list:
            # for design
            spaces = 0
            lines += " " * spaces + i + "\n"

        return lines

    def make_exclusive(self, *args):
        """
        format args
        """
        args = [i[0] if type(i) != str else i for i in args]
        return self.exclusive_str.format(self.or_str.join(args))

    def make_optional(self, *args):
        """
        format args
        """
        args = [i[0] if type(i) != str else i for i in args]
        return self.optional_str.format(self.or_str.join(args))

    def make_user_input(self, *args):
        """
        format args
        """
        # todo make decorator of
        args = [i[0] if type(i) != str else i for i in args]
        return self.user_input_str.format(self.or_str.join(args))

    def get_final_output(self, command=None):
        """
        builds the help menu with the functions above and returns it
        """
        if type(command) == str:
            command = self.get_command_from_chain(command.split())
        elif not isinstance(command, dict):
            command = None

        usage = self.get_usage(command)
        description = self.default_description if command is None else command.get("long_help",
                                                                                   self.default_description)
        help_tree = self.get_help_tree(command)

        # option for later
        # optionals = "Optional:\n{}"
        # for cmd in self.optionals:
        #     optionals += "   {}\n".format(", ".join(self.get_command(cmd).get("opt_str", [])))

        note = ""
        if command:
            note = "Note: {}".format(command.get("note", "")) if command.get("note", "") else ""

        o = [usage, description, help_tree]
        if note:
            o.append(note)
        o.append(self.default_finish_str)

        final_output = "\n\n".join(o)

        return final_output


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
                "opt": [("command", str)],
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
                        "func_name": None,
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
                                        "func_name": None,
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
                                                            "opt": [("force", ["--force", "-f"])]
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
                                                            "opt": [("force", ["--force", "-f"])]
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
                                                            "opt": [("force", ["--force", "-f"])]
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
                                            "opt": [("force", ["--force", "-f"]), ("overwrite", ["--overwrite", "-o"]),
                                                    ("encryption_lvl", int)]
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

    print parameter_structure.get_final_output()
