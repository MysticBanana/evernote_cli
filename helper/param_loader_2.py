# coding=utf-8
import sys
import krypto_manager
import operator

import data.user as udm


class ArgumentParser():
    # require = {username: true/false # if false then username is optional
    # if require = {(username, password): ... # xor
    # if no require and parameter following then xor these

    args_dict = {
        "help":
            {
                "opt_str": ["-h", "--help"],
                "help": "shows this menu or helptext for command",
                "require": {
                    "parameter": False
                }
            },
        "user":
            {
                "opt_str": ["-u", "--user"],
                "help": "used in combination with --new or --passwd",
                "require": {
                    "username": True
                },
                "new_user":
                    {
                        "opt_str": ["-n", "--new"],
                        "help": "create new user",
                        "require": {
                            "token": False
                        }
                    },
                "passwd":
                    {
                        "opt_str": ["-p", "--passwd"],
                        "help": "input your stupid password after",
                        "require": {
                            "password": True
                        },
                        "change":
                            {
                                "opt_str": ["-c", "--change"],
                                "help": "change stuff ",
                                "require": {},
                                "new_pwd":
                                    {
                                        "opt_str": ["-p", "--passwd"],
                                        "help": "change password",
                                        "require": {
                                            "new password": True
                                        }
                                    },
                                "new_path":
                                    {
                                        "opt_str": ["-d", "--downloadpath"],
                                        "help": "change download path",
                                        "require": {
                                            "path": True
                                        }
                                    },
                                "new_encrypt":
                                    {
                                        "opt_str": ["-e", "--encrypt_files"],
                                        "help": "change download encryption level",
                                        "require": {
                                            "encryption lvl": True
                                        }
                                    },
                            },
                        "download":
                            {
                                "opt_str": ["-d", "--download"],
                                "help": "download all files",
                                "require": {
                                    "overwrite": False,
                                    "encryption level": False
                                }
                            },
                        "refresh":
                            {
                                "opt_str": ["-r", "--refresh"],
                                "help": "synchronize your files with the cloud",
                                "require": {}
                            },
                        "encrypt_files":
                            {
                                "opt_str": ["-e", "--encrypt_files"],
                                "help": "encrypting your files",
                                "require": {
                                    "encryption level": False
                                }
                            },
                        "decrypt":
                            {
                                "opt_str": ["-d", "--decrypt"],
                                "help": "decrypting your files",
                                "require": {
                                    "encryption level": False
                                }
                            }
                    }
            }
    }

    def __init__(self, controller, args):
        self.controller = controller

        self.usage = "evernote [-h] [-u <USERNAME> ] ..."
        self.fkt_code = None

        self.error_type = -1

        self.error = {
            0: "To many arguments:\n <rep> arguments were specified, but only a maximum of 8 are allowed",
            1: "To few arguments:\n Only <rep> arguments were specified, but at least 1 argument must be entered",
            2: "One Argument is missing:\n The argument <rep> must be followed by the argument <rep>",
            3: "Authentication failed: "
               "\n If you are using the program for the first time, create a new user with..."
               "\n\t... -u <username> -t <token> <passwd>. "
               "\n Otherwise check if password and username are entered correctly",
            4: "False Parameter:\n The parameter <rep> does not exist in this context",
            5: "You are entered <rep>, but there are only the levels 0, 1, 2, 4"
        }


        self.params = {}

        self.arg_list = args.split()

    def error_msg(self, error_type, argument=[]):
        """
        remove eventually -> DISPLAY MANAGER
        Used to output a error text
        :param error_type:
        :param argument:
        :return:
        """
        inp = "Input: " + str(self.arg_list) + "\n"
        msg = self.error[error_type]
        for i in argument:
            msg = msg.replace("<rep>", i, 1)
        err_msg = inp + self.usage + "\n" + msg + "\n"
        sys.stderr.write(err_msg)
        sys.exit()  # Error Type muss denke ich  geändert werden

    def warning_msg(self, warning_typ=None, arguments=[]):
        """
        remove eventually -> DISPLAY MANAGER
        Used to output a warning text
        :param warning_typ:
        :param arguments:
        :return:
        """
        print "\nWARNING: "
        arg = ""
        for i in arguments:
            arg += i + ", "
        print "Argument(s) " + arg + " have no use and have not been processed"

    def parser(self):
        """
        parses the arguments entered by the user
        :return: Arguments entered by the user
        """
        # Check general number of parameters
        nr_of_args = len(self.arg_list)
        if  nr_of_args == 0:
            self.error_msg(0 if nr_of_args > 8 else 1, [str(nr_of_args)])

        # when entering -h or --help
        if self.arg_list[0] in self.args_dict["help"]["opt_str"]:
            self.params["func"] = "help"

        # when entering (-u | --user) <USERNAME> ...
        elif self.arg_list[0] in self.args_dict["user"]["opt_str"]:
            user_dict = self.args_dict["user"]
            try:
                self.params["username"] = self.arg_list[1]
            except:
                # argument is missing
                self.error_msg(2, ["--user", "<USERNAME>"])

            if nr_of_args < 3:
                # argument is missing
                self.error_msg(2, ["<USERNAME>", "--new OR --passwd"])

            # when entering ... (-n | --new) [<TOKEN>] <PASSWORD>
            if self.arg_list[2] in user_dict["new_user"]["opt_str"]:
                try:
                    if len(self.arg_list) == 5:
                        self.params["token"] = self.arg_list[3]
                        self.params["passwd"] = self.arg_list[4]
                        self.params["password"] = self.arg_list[4]
                        if nr_of_args > 5:
                            self.warning_msg(arguments=self.arg_list[5:])
                    else:
                        self.params["token"] = None
                        self.params["passwd"] = krypto_manager.hash_str(self.arg_list[3])
                        self.params["password"] = self.arg_list[3]
                        if nr_of_args > 4:
                            self.warning_msg(arguments=self.arg_list[4:])
                    self.params["func"] = "new_user"
                except:
                    # argument is missing
                    self.error_msg(2, ["--token", "(<TOKEN> and) <PASSWORD>"])

            # when entering ... (-p | --passwd) <PASSSWORD> ...
            elif self.arg_list[2] in user_dict["passwd"]["opt_str"]:
                passwd_dict = user_dict["passwd"]
                try:
                    passwd_hash = krypto_manager.hash_str(self.arg_list[3])
                    self.params["passwd"] = passwd_hash
                    self.params["password"] = self.arg_list[3]
                except:
                    # argument is missing
                    self.error_msg(2, ["--passwd", "<PASSWORD>"])

                # Check if login data are correct
                check = self.controller.global_data_manager.check_user_hash(self.params["username"],
                                                                            self.params["passwd"])
                if not check:
                    # Authentication failed
                    self.error_msg(3)

                # user = self.controller.global_data_manager.get_user(self.params["username"], self.params["passwd"])

                if nr_of_args < 5:
                    # argument is missing
                    self.error_msg(2, ["<PASSWORD>", "--show, --change, --download, --find, --delete OR --sync"])

                # when entering ... (-c | --change) ...
                if self.arg_list[4] in passwd_dict["change"]["opt_str"]:
                    change_dict = passwd_dict["change"]

                    if nr_of_args < 6:
                        # argument is missing
                        self.error_msg(2, ["--change", "--new_pwd or --downloadpath"])

                    # when entering ... (-p | --passwd) <NEW PASSWORD>
                    if self.arg_list[5] in change_dict["new_pwd"]["opt_str"]:
                        try:
                            self.params["new_pwd"] = self.arg_list[6]
                            self.params["func"] = "new_pwd"
                        except:
                            # argument is missing
                            self.error_msg(2, ["--new_pwd", "<NEW_PWD>"])
                        if nr_of_args > 8:
                            self.warning_msg(arguments=self.arg_list[7:])

                    # when entering ... (-d | --downloadpath) <NEW PATH>
                    elif self.arg_list[5] in change_dict["new_path"]["opt_str"]:
                        try:
                            self.params["new_path"] = self.arg_list[6]
                            self.params["func"] = "new_path"
                        except:
                            # argument is missing
                            self.error_msg(2, ["--new_path", "<NEW_PATH>"])
                        if nr_of_args > 7:
                            self.warning_msg(arguments=self.arg_list[7:])
                    # when entering ... (-e | --encrypt_files) <NEW ENCRYPT LVL>
                    elif self.arg_list[5] in change_dict["new_encrypt"]["opt_str"]:
                        try:
                            encrypt_lvl = int(self.arg_list[6])
                            if encrypt_lvl in [0, 1, 2, 3, 4]:
                                self.params["new_encrypt_lvl"] = encrypt_lvl
                            else:
                                self.error_msg(5, [str(encrypt_lvl)])
                            self.params["func"] = "new_encrypt_lvl"
                        except IndexError:
                            # argument is missing
                            self.error_msg(2, ["--encrypt_files", "<NEW_ENCRYPTION_LVL>"])
                        except :
                            self.error_msg(4, self.arg_list[6])
                        if nr_of_args > 7:
                            self.warning_msg(arguments=self.arg_list[7:])
                    else:
                        # False Parameter
                        self.error_msg(4, self.arg_list[5])

                # when entering ... (-d | --download) [<OVERWRITE>] [<ENCRYPTION LVL>]
                elif self.arg_list[4] in passwd_dict["download"]["opt_str"]:
                    self.params["func"] = "download"
                    if nr_of_args == 5:
                        self.params["encryption_lvl"] = -1
                        self.params["overwrite"] = False
                    else:
                        try:
                            encrypt_lvl = int(self.arg_list[5])
                            if encrypt_lvl not in [0, 1, 2, 4]:
                                # False Encryption Level selected
                                self.error_msg(5, [str(encrypt_lvl)])
                            self.params["encryption_lvl"] = encrypt_lvl
                            self.params["overwrite"] = False
                            if nr_of_args > 6:
                                self.warning_msg(arguments=self.arg_list[6:])
                        except Exception:
                            overwrite = self.arg_list[5]
                            if overwrite != "-o":
                                self.error_msg(4, [self.arg_list[5]])
                            self.params["overwrite"] = True
                            if nr_of_args == 6:
                                self.params["encryption_lvl"] = -1
                            elif nr_of_args >= 7:
                                try:
                                    encrypt_lvl = int(self.arg_list[6])
                                    if encrypt_lvl not in [0, 1, 2, 4]:
                                        # False Encryption Level selected
                                        self.error_msg(5, [str(encrypt_lvl)])
                                    self.params["encryption_lvl"] = encrypt_lvl
                                    if nr_of_args >= 8:
                                        self.warning_msg(arguments=self.arg_list[7:])
                                except Exception:
                                    self.warning_msg(arguments=self.arg_list[6:])


                # when entering ... (-r | --refresh)
                elif self.arg_list[4] in passwd_dict["refresh"]["opt_str"]:
                    self.params["func"] = "refresh"
                    if nr_of_args > 5:
                        self.warning_msg(arguments=self.arg_list[5:])

                # when entering ... (-e | --encrypt_files) [<ENCRYPTION LVL>]
                elif self.arg_list[4] in passwd_dict["encrypt_files"]["opt_str"]:
                    self.params["func"] = "encrypt_files"
                    if nr_of_args >= 6:
                        try:
                            encrypt_lvl = int(self.arg_list[5])
                            if encrypt_lvl not in [0, 1, 2, 4]:
                                # False Encryption Level selected
                                self.error_msg(5, [str(encrypt_lvl)])
                            self.params["encryption_lvl"] = encrypt_lvl
                            if nr_of_args >= 7:
                                self.warning_msg(arguments=self.arg_list[6:])
                        except Exception:
                            self.params["encryption_lvl"] = -1
                            self.warning_msg(arguments=self.arg_list[5:])
                    else:
                        self.params["encryption_lvl"] = -1

                # when entering ... (-de | --decrypt)
                elif self.arg_list[4] in passwd_dict["decrypt"]["opt_str"]:
                    self.params["func"] = "decrypt"
                    if nr_of_args > 5:
                        self.warning_msg(arguments=self.arg_list[5:])
                else:
                    # false parameter
                    self.error_msg(4, [self.arg_list[4]])
            else:
                # false parameter
                self.error_msg(4, [self.arg_list[2]])
        else:
            # false parameter
            self.error_msg(4, [self.arg_list[2]])
        return self.params
