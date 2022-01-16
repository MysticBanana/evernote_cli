# coding=utf-8
import krypto_manager
import copy

'''
$ evernote ...
    -h | --help
    -u | -- user <Username> ...
        -n | --new <Passwd> [<Token>]
        -p | --passwd <Passwd> ...
            -c | --change [-f]...
                -p | --passwd <New_Passwd>
                -d | --downloadpath <New_path>
                -e | --encrypt <New encrypion lvl>
            -d | --download [-f] [<Overwrite>] [<Encryption_Lvl>]
            -e | --encrypt [<Encryption_Lvl>]
            -de | --decrypt
            -r | --refresh
            -rm | --remove
'''

class ArgumentParser:

    def __init__(self, controller, args):
        self.controller = controller

        self.arg_list = args.split()
        self.arguments = {
            "help":
                {
                    "opt_str": ["-h", "--help"],
                    "help": "shows this menu or helptext for command",
                    "func": True,
                    "func_name": "help",
                    "require": {
                        "parameter": False,
                    },
                    "next_args": {
                        "none_opt" : None,
                        "opt": [("param", str)]
                    },
                    "next_params" : None
                },
            "user":
                {
                    "opt_str": ["-u", "--user"],
                    "help": "used in combination with --new or --passwd",
                    "func": False,
                    "func_name": None,
                    "require": {
                        "username": True
                    },
                    "next_args": {
                        "none_opt": ["username"],
                        "opt": None
                    },
                    "next_params":
                        {
                            "new_user":
                                {
                                    "opt_str": ["-n", "--new"],
                                    "help": "create new user",
                                    "func": True,
                                    "func_name": "new_user",
                                    "require": {
                                        "token": False
                                    },
                                    "next_args": {
                                        "none_opt": ["password"],
                                        "opt": [("token", str)]
                                    },
                                    "next_params": None
                                },
                            "passwd":
                                {
                                    "opt_str": ["-p", "--passwd"],
                                    "help": "input your stupid password after",
                                    "func": False,
                                    "func_name": None,
                                    "require": {
                                        "password": True
                                    },
                                    "next_args": {
                                        "none_opt": ["password"],
                                        "opt": None
                                    },
                                    "next_params":
                                        {
                                            "change":
                                                {
                                                    "opt_str": ["-c", "--change"],
                                                    "help": "change stuff ",
                                                    "func": False,
                                                    "func_name": None,
                                                    "require": {
                                                        "force": False
                                                    },
                                                    "next_args": None,
                                                    "next_params":
                                                        {
                                                            "new_pwd":
                                                                {
                                                                    "opt_str": ["-p", "--passwd"],
                                                                    "help": "change password",
                                                                    "func": True,
                                                                    "func_name": "new_pwd",
                                                                    "require": {
                                                                        "new password": True
                                                                    },
                                                                    "next_args": {
                                                                        "none_opt": ["new_password"],
                                                                        "opt": [("force", "-f")]
                                                                    },
                                                                    "next_params": None
                                                                },
                                                            "new_path":
                                                                {
                                                                    "opt_str": ["-d", "--downloadpath"],
                                                                    "help": "change download path",
                                                                    "func": True,
                                                                    "func_name": "new_path",
                                                                    "require": {
                                                                        "path": True
                                                                    },
                                                                    "next_args": {
                                                                        "none_opt": ["new_path"],
                                                                        "opt": [("force", "-f")]
                                                                    },
                                                                    "next_params": None
                                                                },
                                                            "new_encrypt":
                                                                {
                                                                    "opt_str": ["-e", "--encrypt_files"],
                                                                    "help": "change download encryption level",
                                                                    "func": True,
                                                                    "func_name": "new_encrypt",
                                                                    "require": {
                                                                        "encryption lvl": True
                                                                    },
                                                                    "next_args": {
                                                                        "none_opt": [("new_encrypt_lvl", int)],
                                                                        "opt": [("force", "-f")]
                                                                    },
                                                                    "next_params": None
                                                                },
                                                        }
                                                },
                                            "download":
                                                {
                                                    "opt_str": ["-d", "--download"],
                                                    "help": "download all files",
                                                    "func": True,
                                                    "func_name": "download",
                                                    "require": {
                                                        "overwrite": False,
                                                        "encryption level": False
                                                    },
                                                    "next_args": {
                                                        "none_opt": None,
                                                        "opt": [("force", "-f"),("overwrite", "-o"),("encrypt_lvl", int)]
                                                    },
                                                    "next_params": None
                                                },
                                            "encrypt":
                                                {
                                                    "opt_str": ["-e", "--encrypt"],
                                                    "help": "encrypting your files",
                                                    "func": True,
                                                    "func_name": "encrypt",
                                                    "require": {
                                                        "encryption level": False
                                                    },
                                                    "next_args": {
                                                        "none_opt": None,
                                                        "opt": [("encrypt_lvl", int)]
                                                    },
                                                    "next_params": None
                                                },
                                            "decrypt":
                                                {
                                                    "opt_str": ["-de", "--decrypt"],
                                                    "help": "decrypting your files",
                                                    "func": True,
                                                    "func_name": "decrypt",
                                                    "require": {
                                                        "encryption level": False
                                                    },
                                                    "next_args": None,
                                                    "next_params": None
                                                },
                                            "refresh":
                                                {
                                                    "opt_str": ["-r", "--refresh"],
                                                    "help": "synchronize your files with the cloud",
                                                    "func": True,
                                                    "func_name": "refresh",
                                                    "require": {},
                                                    "next_args": None,
                                                    "next_params": None
                                                },
                                            "remove":
                                                {
                                                    "opt_str": ["-rm", "--remove"],
                                                    "help": "remove user",
                                                    "func": True,
                                                    "func_name": "remove",
                                                    "require": {},
                                                    "next_args": None,
                                                    "next_params": None
                                                }
                                        }
                                }
                        }
                }
        }
        self.params = {}

        self.wrong_input = False

    def error(self, msg):
        self.params = {"func": "error", "err_typ": msg}

    def add_input_check_error(self, input_typ, user_input):
        if not self.wrong_input:
            self.params = {"func": "input_error", "err_types": []}
        self.params["err_types"].append((input_typ, user_input))

    def warning(self, msg):
        print "Warning: {}".format(msg)

    def get_next_params(self, arguments):
        next_params, next_arg = None, None
        param = self.arg_list.pop(0)
        dict_len = len(self.params)
        end = True
        correct_param = False
        for key, _ in arguments.items():
            if param in arguments[key]["opt_str"]:
                correct_param = True
                next_params = arguments[key]["next_params"]
                if arguments[key]["func"]:
                    self.params["func"] = arguments[key]["func_name"]
                else:
                    end = False
                if not arguments[key]["next_args"] == None:
                    if not arguments[key]["next_args"]["none_opt"] == None:
                        self.get_args(arguments[key]["next_args"]["none_opt"]) # TODO implement
                    if not arguments[key]["next_args"]["opt"] == None:
                        self.get_opt_args(arguments[key]["next_args"]["opt"])
        if not correct_param:
            self.error("{} is wrong".format(param))
            return None, True
        return next_params, end

    def get_args(self, args):
        try:
            for arg in args:
                if len(self.arg_list) == 0:
                    self.error("Parameter fehlen")
                    break
                if type(arg) == type((1,1)):
                    try:
                        self.params[arg[0]] = int(self.arg_list.pop(0))
                    except:
                        self.params[arg[0]] = -1
                    continue
                self.params[arg] = self.arg_list.pop(0)
        except:
            self.error("Parameter fehlen")

    def get_opt_args(self, opt_args):
        for arg, typ in opt_args:
            # z.B. arg = "param"; typ = int
            if type(typ) == type(int):
                try:
                    self.params[arg] = typ(self.arg_list[0])
                    self.arg_list.pop(0)
                except:
                    self.params[arg] = None
            # z.B. arg = "param"; typ = "-f"
            else:
                if len(self.arg_list) == 0:
                    self.params[arg] = False
                    continue
                if self.arg_list[0] == typ:
                    self.params[arg] = True
                    self.arg_list.pop(0)
                else:
                    self.params[arg] = False

    def parser(self):
        nr_of_args = len(self.arg_list)
        # Check general number of parameters
        if nr_of_args == 0:
            # TODO: ERROR ersetzen
            self.error("Keine Parameter")
            return
        end = False
        next_param = self.arguments

        while not end:
            if len(self.arg_list) == 0:
                self.error("es fehlen parameter")
                break
            next_param, end = self.get_next_params(next_param)

        # add password hash to self.params
        self.params["password_hash"] = krypto_manager.hash_str(self.params["password"])

        #User Input Check
        params = copy.deepcopy(self.params)

        if not self.params["func"] == "new_user":
            # Check if login data are correct
            check = self.controller.global_data_manager.check_user_hash(self.params["username"], self.params["password_hash"])
            if not check:
                # Authentication failed
                self.add_input_check_error("authentication", [self.params["username"], self.params["password"]])
            for key, val in params.items():
                if key == "encrypt_lvl" or key == "new_encrypt_lvl":
                    print val
                    print self.controller.max_encryption_level
                    if 0 > val > self.controller.max_encryption_level:
                        # False Encryption Level selected
                        self.add_input_check_error(key, val)

        if not len(self.arg_list) == 0:
            self.warning("{} wurde ignoriert".format(self.arg_list))
