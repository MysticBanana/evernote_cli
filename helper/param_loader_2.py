# coding=utf-8
import sys
import krypto_manager
import operator


def new_user(params):
    print "CREATE new User:"
    print "\tusername=" + params["username"]
    print "\ttoken=" + params["token"]
    print "\tpasswd=" + params["passwd"]


def passwd_check(params):
    if params["username"] == "user":
        if params["passwd"] == "userpwd":
            return True
    return False


def show_path(params):
    print "SHOW:"
    print "\tfile: " + params["path"]


def show_userdata(params):
    print "SHOW:" \
          "\tuserdata from: " + params["username"]


def change_passwd(params):
    print "CHANGE PWD: "
    print "\told pwd: " + params["passwd"]
    print "\tnew pwd: " + params["new_pwd"]


def change_path(params):
    print "CHANGE PATH: "
    print "\told path: ...."
    print "\tnew path: " + params["new_path"]


def download(params=None):
    print "DOWNLOAD: "
    if params == None:
        print "\tALL"
    else:
        print "\tREST"


def find(params):
    print "FIND: "
    print "\t" + params["find"]


def refresh():
    print "REFRESH"


class ArgumentParser():
    args_dict = dict()

    def __init__(self, controller, args):
        self.controller = controller

        self.usage = "evernote [-h] [-u <USERNAME> ] ..."
        self.fkt_code = None

        self.error_type = -1

        self.error = {
            0: "To many arguments:\n <rep> arguments were specified, but only a maximum of 8 are allowed",
            1: "To few arguments:\n Only <rep> arguments were specified, but at least 1 argument must be entered",
            2: "One Argument is missing:\n The argument <rep> must be followed by the argument <rep>",
            3: "Authentification failed: "
               "\n If you are using the program for the first time, create a new user with..."
               "\n\t... -u <username> -t <token> <passwd>. "
               "\n Otherwise check if password and username are entered correctly",
            4: "False Parameter:\n The parameter <rep> does not exist in this context"
        }

        self.function = {
            "help": self.help_msg,
            "new_user": new_user,
            "show_path": show_path,
            "show_userdata": show_userdata,
            "new_pwd": change_passwd,
            "new_path": change_path,
            "download": download,
            "find": find,
            "refresh": refresh
        }

        self.args_dict = {
            "help":
                {
                    "contains_args": False,
                    "opt_str": ["-h", "--help"],
                    "help_msg": "Show this help message and exit"
                },
            "user":
                {
                    "contains_args": True,
                    "opt_str": ["-u", "--user"],
                    "help_msg": "Actions that users need",
                    "username":
                        {
                            "contains_args": False,
                            "opt_str": ["<USERNAME>"],
                            "help_msg": "the name of the user in Evernote",
                        },
                    "token":
                        {
                            "contains_args": True,
                            "opt_str": ["-t", "--token"],
                            "help_msg": "Token is required for first time use",
                            "token_arg":
                                {
                                    "contains_args": False,
                                    "opt_str": ["<TOKEN>"],
                                    "help_msg": "the User-Token for evernote",
                                },
                            "passwd_arg":
                                {
                                    "contains_args": False,
                                    "opt_str": ["<PASSWORD>"],
                                    "help_msg": "the user's self-selected password",
                                }
                        },
                    "passwd":
                        {
                            "contains_args": True,
                            "opt_str": ["-p", "--passwd"],
                            "help_msg": "\bActions that require authentication by password",
                            "passwd_arg":
                                {
                                    "contains_args": False,
                                    "opt_str": ["<PASSWORD>"],
                                    "help_msg": "HELPMSG FOR PASSWD_ARG?"
                                },
                            "show":
                                {
                                    "contains_args": True,
                                    "opt_str": ["-s", "--show"],
                                    "help_msg": "HELPMSG FOR SHOW?",
                                    "file":
                                        {
                                            "contains_args": True,
                                            "opt_str": ["-f", "--file"],
                                            "help_msg": "HELPMSG FOR SHOW FILE?",
                                            "path_arg":
                                                {
                                                    "contains_args": False,
                                                    "opt_str": ["<PATH|NOTE|NOTEBOOK>"],
                                                    "help_msg": "\b\b\bHELPMSG FOR SHOW FILE PATH?",
                                                }
                                        },
                                    "userdata":
                                        {
                                            "contains_args": False,
                                            "opt_str": ["-u", "--userdata"],
                                            "help_msg": "\bHELPMSG FOR SHOW USERDATA?",
                                        },
                                    "path":
                                        {
                                            "contains_args": True,
                                            "opt_str": ["-p", "--path"],
                                            "help_msg": "HELPMSG FOR SHOW PATH?",
                                            "path":
                                                {
                                                    "contains_args": False,
                                                    "opt_str": ["<NOTE|NOTEBOOK>"],
                                                    "help_msg": "\b\bHELPMSG FOR SHOW PATH PATH_ARG?",
                                                }
                                        }
                                },
                            "change":
                                {
                                    "contains_args": True,
                                    "opt_str": ["-c", "--change"],
                                    "help_msg": "\bHELPMSG FOR CHANGE?",
                                    "new_pwd":
                                        {
                                            "contains_args": True,
                                            "opt_str": ["-b", "--passwd"],
                                            "help_msg": "\bHELPMSG FOR CHANGE NEW_PWD?",
                                            "new_pwd_arg":
                                                {
                                                    "contains_args": False,
                                                    "opt_str": ["<NEW_PWD>"],
                                                    "help_msg": "HELPMSG FOR CHANGE NEW_PWD <NEW_PWD>?"
                                                }
                                        },
                                    "new_path":
                                        {
                                            "contains_args": True,
                                            "opt_str": ["-d", "--downloadpath"],
                                            "help_msg": "\b\bHELPMSG FOR CHANGE NEW_PATH?",
                                            "new_pwd_arg":
                                                {
                                                    "contains_args": False,
                                                    "opt_str": ["<NEW_PATH>"],
                                                    "help_msg": "HELPMSG FOR CHANGE NEW_PATH <NEW_PATH>?"
                                                }
                                        }
                                },
                            "download":
                                {
                                    "contains_args": True,
                                    "opt_str": ["-d", "--download"],
                                    "help_msg": "\bHELPMSG FOR DOWNLOAD",
                                    "all":
                                        {
                                            "contains_args": False,
                                            "opt_str": ["-a", "--all"],
                                            "help_msg": "\bHELPMSG FOR DOWNLOAD ALL"
                                        }
                                },
                            "find":
                                {
                                    "contains_args": True,
                                    "opt_str": ["-f", "--find"],
                                    "help_msg": "HELPMSG FOR FIND",
                                    "find_arg":
                                        {
                                            "contains_args": False,
                                            "opt_str": ["<TAG|NOTENAME|NOTEBOOKNAME>"],
                                            "help_msg": "\b\b\b\b\bHELPMSG FOR FIND ARG",
                                        }
                                },
                            "refresh":
                                {
                                    "contains_args": False,
                                    "opt_str": ["-r", "--refresh"],
                                    "help_msg": "\bHELPMSG FOR REFRESH"
                                }
                        }
                }
        }
        self.params = {}

        self.arg_list = args.split()

    # Erstellen von Hilfe-Nachrichten
    def help_msg(self, arg_dict, seperator="", lvl=0):
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

    # Erstellt Error-Messages
    def error_msg(self, error_type, argument=[]):
        inp = "Input: " + str(self.arg_list) + "\n"
        msg = self.error[error_type]
        for i in argument:
            msg = msg.replace("<rep>", i, 1)
        err_msg = inp + self.usage + "\n" + msg
        sys.stderr.write(err_msg)
        sys.exit()  # Error Type muss denke ich  geändert werden

    def warning_msg(self, warning_typ=None, arguments=[]):
        print "\nWARNING: "
        arg = ""
        for i in arguments:
            arg += i + ", "
        print "Argument(s) " + arg + " have no use and have not been processed"

    def parser(self):
        nr_of_args = len(self.arg_list)
        # allg. Anzahl der Parameter prüfen
        if nr_of_args > 7 or nr_of_args == 0:
            self.error_msg(0 if nr_of_args > 8 else 1, [str(nr_of_args)])

        # Bei Eingabe von "-h"
        if self.arg_list[0] in self.args_dict["help"]["opt_str"]:
            self.function["help"](self.args_dict)

        # Bei Eingabe von "-u <Username> ..."
        elif self.arg_list[0] in self.args_dict["user"]["opt_str"]:
            user_dict = self.args_dict["user"]
            try:
                self.params["username"] = self.arg_list[1]
            except:
                self.error_msg(2, ["--user", "<USERNAME>"])

            if nr_of_args < 3:
                self.error_msg(2, ["<USERNAME>", "--token OR --passwd"])

            # Bei Eingabe von "-u <Username> -t <Token> <Passwd>"
            if self.arg_list[2] in user_dict["token"]["opt_str"]:
                try:
                    self.params["token"] = self.arg_list[3]
                    self.params["passwd"] = self.arg_list[4]
                    self.function["new_user"](self.params)
                    if nr_of_args > 5:
                        self.warning_msg(arguments=self.arg_list[5:])
                except:
                    self.error_msg(2, ["--token", "<TOKEN> and <PASSWORD>"])

            # Bei Eingabe von "-u <Username> -p <Passwd> ..."
            elif self.arg_list[2] in user_dict["passwd"]["opt_str"]:
                passwd_dict = user_dict["passwd"]
                try:
                    self.params["passwd"] = self.arg_list[3]
                except:
                    self.error_msg(2, ["--passwd", "<PASSWORD>"])

                passwd_hash = krypto_manager.hash_str(self.params["passwd"])
                check = self.controller.global_data_manager.check_user_hash(self.params["username"], passwd_hash)
                if not check:
                    self.error_msg(3)

                if nr_of_args < 5:
                    self.error_msg(2, ["<PASSWORD>", "--show, --change, --download, --find, --delete OR --sync"])

                # Bei Eingabe von "-u <Username> -p <Passwd> -s ...
                if self.arg_list[4] in passwd_dict["show"]["opt_str"]:
                    show_dict = passwd_dict["show"]

                    if nr_of_args < 6:
                        self.error_msg(2, ["--show", "--file, --userdata or --path"])

                    # Bei Eingabe von "-u <Username> -p <Passwd> -s -f <PATH|NOTE|NOTEBOOK>
                    if self.arg_list[5] in show_dict["file"]["opt_str"]:
                        try:
                            self.params["file"] = self.arg_list[6]
                            self.function["show_file"](self.params)
                        except:
                            self.error_msg(2, ["--file", "<PATH|NOTE|NOTEBOOK>"])

                    # Bei Eingabe von "-u <Username> -p <Passwd> -s -u
                    elif self.arg_list[5] in show_dict["userdata"]["opt_str"]:
                        self.function["show_userdata"](self.params)

                    # Bei Eingabe von "-u <Username> -p <Passwd> -s -p <NOTE|NOTEBOOK>
                    elif self.arg_list[5] in show_dict["path"]["opt_str"]:
                        try:
                            self.params["path"] = self.arg_list[6]
                            self.function["show_path"](self.params)
                        except:
                            self.error_msg(2, ["--path", "<NOTE|NOTEBOOK>"])
                    else:
                        self.error_msg(4, self.arg_list[5])

                # Bei Eingabe von "-u <Username> -p <Passwd> -c ...
                elif self.arg_list[4] in passwd_dict["change"]["opt_str"]:
                    change_dict = passwd_dict["change"]

                    if nr_of_args < 6:
                        self.error_msg(2, ["--change", "--new_pwd or --download_path"])

                    # Bei Eingabe von "-u <Username> -p <Passwd> -c -b <NEW_PWD>
                    if self.arg_list[5] in change_dict["new_pwd"]["opt_str"]:
                        try:
                            self.params["new_pwd"] = self.arg_list[6]
                            self.function["new_pwd"](self.params)
                        except:
                            self.error_msg(2, ["--new_pwd", "<NEW_PWD>"])

                    # Bei Eingabe von "-u <Username> -p <Passwd> -c -d <new_path>
                    elif self.arg_list[5] in change_dict["new_path"]["opt_str"]:
                        try:
                            self.params["new_path"] = self.arg_list[6]
                            self.function["new_path"](self.params)
                        except:
                            self.error_msg(2, ["--new_path", "<NEW_PATH>"])
                    else:
                        self.error_msg(4, self.arg_list[5])

                # Bei Eingabe von "-u <Username> -p <Passwd> -d ...
                elif self.arg_list[4] in passwd_dict["download"]["opt_str"]:
                    download_dict = passwd_dict["download"]

                    if nr_of_args < 6:
                        self.error_msg(2, ["--download", "--all"])

                    # Bei Eingabe von "-u <Username> -p <Passwd> -d -a
                    if self.arg_list[5] in download_dict["all"]["opt_str"]:
                        self.function["download"]()
                        if nr_of_args > 6:
                            self.warning_msg(arguments=self.arg_list[6:])
                    else:
                        self.error_msg(4, self.arg_list[5])

                # Bei Eingabe von "-u <Username> -p <Passwd> -f <TAG|NOTENAME|NOTEBOOKNAME>
                elif self.arg_list[4] in passwd_dict["find"]["opt_str"]:
                    try:
                        self.params["find"] = self.arg_list[5]
                        self.function["find"](self.params)
                        if nr_of_args > 6:
                            self.warning_msg(arguments=self.arg_list[6:])
                    except:
                        self.error_msg(2, ["--find", "<TAG|NOTENAME|NOTEBOOKNAME>"])

                # Bei Eingabe von "-u <Username> -p <Passwd> -r
                elif self.arg_list[4] in passwd_dict["refresh"]["opt_str"]:
                    self.function["refresh"]()
                    if nr_of_args > 5:
                        self.warning_msg(arguments=self.arg_list[5:])
                else:
                    self.error_msg(4, self.arg_list[4])


if __name__ == "__main__":
    user = "mneuhaus"
    password = "test1234"

    par = ArgumentParser(None, "-h")
    print par.args_dict.items()

