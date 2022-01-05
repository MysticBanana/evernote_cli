# coding=utf-8
import sys
import krypto_manager
import operator

import data.user_data_manager as udm


class ArgumentParser():
    args_dict = {
        "help":
            {
                "opt_str": ["-h", "--help"],
            },
        "user":
            {
                "opt_str": ["-u", "--user"],
                "new_user":
                    {
                        "opt_str": ["-n", "--new"],
                    },
                "passwd":
                    {
                        "opt_str": ["-p", "--passwd"],
                        "change":
                            {
                                "opt_str": ["-c", "--change"],
                                "new_pwd":
                                    {
                                        "opt_str": ["-p", "--passwd"],
                                    },
                                "new_path":
                                    {
                                        "opt_str": ["-d", "--downloadpath"],
                                    }
                            },
                        "download":
                            {
                                "opt_str": ["-d", "--download"],
                            },
                        "refresh":
                            {
                                "opt_str": ["-r", "--refresh"],
                            },
                        "encrypt":
                            {
                                "opt_str": ["-e", "--encrypt"],
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
            4: "False Parameter:\n The parameter <rep> does not exist in this context"
        }


        self.params = {}

        self.arg_list = args.split()

    def help_msg(self, arg_dict, seperator="", lvl=0):
        """
        remove eventually -> DISPLAY MANAGER
        Used to output a help text
        :param arg_dict:
        :param seperator:
        :param lvl:
        :return:
        """
        sep = seperator
        for i in dict(sorted(arg_dict.items(), key=operator.itemgetter(0))):
            if i in ["contains_args", "opt_str", "help_msg", "idx"]:
                continue
            opt_str = ""
            for opt in arg_dict[i]["opt_str"]:
                opt_str += opt + " "
            print sep + opt_str + "\t" * (9 - lvl) + arg_dict[i]["help_msg"]
            if arg_dict[i]["contains_args"]:
                self.help_msg(arg_dict[i], sep + "\t", lvl + 1)

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
        err_msg = inp + self.usage + "\n" + msg
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

            # when entering ... (-n | --new) [<TOKEN>] <PASSWORD> ...
            if self.arg_list[2] in user_dict["new_user"]["opt_str"]:
                try:
                    if len(self.arg_list) == 5:
                        self.params["token"] = self.arg_list[3]
                        self.params["passwd"] = self.arg_list[4]
                        if nr_of_args > 5:
                            self.warning_msg(arguments=self.arg_list[5:])
                    else:
                        self.params["token"] = None
                        self.params["passwd"] = self.arg_list[3]
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
                except:
                    # argument is missing
                    self.error_msg(2, ["--passwd", "<PASSWORD>"])

                # Check if login data are correct
                check = self.controller.global_data_manager.check_user_hash(self.params["username"],
                                                                            self.params["passwd"])
                if not check:
                    # Authentication failed
                    self.error_msg(3)

                if nr_of_args < 5:
                    # argument is missing
                    self.error_msg(2, ["<PASSWORD>", "--show, --change, --download, --find, --delete OR --sync"])
                '''
                # when entering ... [-s | --show] ...
                if self.arg_list[4] in passwd_dict["show"]["opt_str"]:
                    show_dict = passwd_dict["show"]

                    if nr_of_args < 6:
                        # argument is missing
                        self.error_msg(2, ["--show", "--file, --userdata or --path"])

                    # Bei Eingabe von "-u <Username> -p <Passwd> -s -f <PATH|NOTE|NOTEBOOK>
                    if self.arg_list[5] in show_dict["file"]["opt_str"]:
                        try:
                            self.params["file"] = self.arg_list[6]
                            self.params["func"] = "show_file"
                        except:
                            self.error_msg(2, ["--file", "<PATH|NOTE|NOTEBOOK>"])

                    # Bei Eingabe von "-u <Username> -p <Passwd> -s -u
                    elif self.arg_list[5] in show_dict["userdata"]["opt_str"]:
                        self.params["func"] = "show_userdata"

                    # Bei Eingabe von "-u <Username> -p <Passwd> -s -p <NOTE|NOTEBOOK>
                    elif self.arg_list[5] in show_dict["path"]["opt_str"]:
                        try:
                            self.params["path"] = self.arg_list[6]
                            self.params["func"] = "show_path"
                        except:
                            self.error_msg(2, ["--path", "<NOTE|NOTEBOOK>"])
                    else:
                        self.error_msg(4, self.arg_list[5])
                ''' # show

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
                    else:
                        # False Parameter
                        self.error_msg(4, self.arg_list[5])
                # TODO Encrypt levl und overwrite unabhängig machen
                # when entering ... (-d | --download) [<ENCRYPTION LVL>] [<OVERWRITE>]
                elif self.arg_list[4] in passwd_dict["download"]["opt_str"]:
                    self.params["func"] = "download"
                    if len(self.arg_list) == 7:
                        if self.arg_list[5] in [0, 1, 2, 3]:
                            self.params["encrypt_lvl"] = self.arg_list[5]
                        else:
                            # False Parameter
                            self.error_msg(4, self.arg_list[5])
                        if self.arg_list[6] in "-o":
                            self.params["overwrite"] = True
                    else:
                        self.params["encrypt_lvl"] = 0
                        self.params["overwrite"] = False
                    if nr_of_args > 7:
                        self.warning_msg(arguments=self.arg_list[6:])

                # Bei Eingabe von "-u <Username> -p <Passwd> -f <TAG|NOTENAME|NOTEBOOKNAME>
                #elif self.arg_list[4] in passwd_dict["find"]["opt_str"]:
                #    try:
                #        self.params["find"] = self.arg_list[5]
                #        self.params["func"] = "find"
                #       if nr_of_args > 6:
                #            self.warning_msg(arguments=self.arg_list[6:])
                #    except:
                #        self.error_msg(2, ["--find", "<TAG|NOTENAME|NOTEBOOKNAME>"])


                # when entering ... (-r | --refresh)
                elif self.arg_list[4] in passwd_dict["refresh"]["opt_str"]:
                    self.params["func"] = "refresh"
                    if nr_of_args > 5:
                        self.warning_msg(arguments=self.arg_list[5:])

                # when entering ... (-e | --encrypt)
                elif self.arg_list[4] in passwd_dict["encrypt"]["opt_str"]:
                    self.params["func"] = "encrypt"
                    if nr_of_args > 5:
                        self.warning_msg(arguments=self.arg_list[5:])
                # when entering ... (-e | --encrypt)
                elif self.arg_list[4] in passwd_dict["decrypt"]["opt_str"]:
                    self.params["func"] = "decrypt"
                    if nr_of_args > 5:
                        self.warning_msg(arguments=self.arg_list[5:])
                else:
                    # false parameter
                    self.error_msg(4, self.arg_list[4])

        return self.params
