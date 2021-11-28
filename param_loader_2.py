# coding=utf-8
import sys
import json

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



class ArgumentParser():
    args_dict = dict()

    def __init__(self, args):
        self.usage = "evernote [-h] [-u <USERNAME> ] ..."
        self.fkt_code = None

        self.error_type = -1

        self.error = {
            0: "To many arguments:\n <rep> arguments were specified, but only a maximum of 8 are allowed",
            1: "To few arguments:\n Only <rep> arguments were specified, but at least 1 argument must be entered",
            2: "One Argument is missing:\n The argument <rep> must be followed by the argument <rep>",
            3: "Two Arguments are missing:\n The argument <rep> must be followed by the arguments <rep> and <rep>",
            4: "Authentification failed: "
               "\n If you are using the program for the first time, create a new user with..."
               "\n\t... -u <username> -t <token> <passwd>. "
               "\n Otherwise check if password and username are entered correctly"

        }
        self.function = {
            "help": self.help_msg,
            "new_user": new_user,
            "passwd_check": passwd_check
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
                            "token":
                                {
                                    "contains_args": False,
                                    "opt_str": ["<TOKEN>"],
                                    "help_msg": "the User-Token for evernote",
                                },
                            "passwd":
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
                            "show":
                                {
                                    "contains_args": True,
                                    "opt_str": ["-s", "--show"],
                                    "help_msg": "HELPMSG FOR SHOW?"
                                }
                        }
                }
        }
        self.params = {}

        self.arg_list = args.split()

    # Erstellen von Hilfe-Nachrichten
    def help_msg(self, arg_dict, seperator="", lvl=0):
        sep = seperator
        for i in arg_dict:
            if i in ["contains_args", "opt_str", "help_msg"]:
                continue
            opt_str = ""
            for opt in arg_dict[i]["opt_str"]:
                opt_str += opt + " "
            print sep + opt_str + "\t"*(5-lvl) + arg_dict[i]["help_msg"]
            if arg_dict[i]["contains_args"]:
                self.help_msg(arg_dict[i], sep + "\t", lvl+1)


    # Erstellt Error-Messages
    def error_msg(self, error_type, argument=[]):
        inp = "Input: " + str(self.arg_list) + "\n"
        msg = self.error[error_type]
        for i in argument:
            msg = msg.replace("<rep>", i, 1)
        err_msg = inp + self.usage + "\n" + msg
        sys.stderr.write(err_msg)
        sys.exit(error_type)    # Error Type muss denke ich  geändert werden

    def parser(self):
        nr_of_args = len(self.arg_list)
        # allg. Anzahl der Parameter prüfen
        if nr_of_args > 8 or nr_of_args == 0:
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
                except:
                    self.error_msg(3, ["--token", "<TOKEN>", "<PASSWORD>"])

            # Bei Eingabe von "-u <Username> -p <Passwd> ..."
            elif self.arg_list[2] in user_dict["passwd"]["opt_str"]:
                passwd_dict = user_dict["passwd"]
                try:
                    self.params["passwd"] = self.arg_list[3]
                except:
                    self.error_msg(2, ["--passwd", "<PASSWORD>"])
                if not self.function["passwd_check"](self.params):
                    self.error_msg(4)
                if nr_of_args < 5:
                    self.error_msg(2, ["<PASSWORD>", "--show, --change, --download, --find, --delete OR --sync"])

                # Bei Eingabe von "-u <Username> -p <Passwd> -s ...
                # Bei Eingabe von "-u <Username> -p <Passwd> -s ...
                # Bei Eingabe von "-u <Username> -p <Passwd> -s ...
                # Bei Eingabe von "-u <Username> -p <Passwd> -s ...
                # Bei Eingabe von "-u <Username> -p <Passwd> -s ...
                # Bei Eingabe von "-u <Username> -p <Passwd> -s ...

if __name__ == "__main__":
    par = ArgumentParser("-h")
    par.parser()
    for k, v in par.params.items():
        print k + "=" + v