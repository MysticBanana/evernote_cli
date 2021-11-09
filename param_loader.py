from sys import argv
import argparse
import sys

'''
$evernote [options]

options:
    -l [LOGLEVEL]       Evernote-Logdatei anzeigen
    -h 
    -u <USERNAME> [arg]
        arg:
            -t <TOKEN> PASSWORD                 -> Create new USER 
            -p <PASSWORD>  [
                -v [arg]                        -> show ...
                    arg:
                        -f <PATH|NOTE|NOTEBOOK> -> ... FILE
                        -u <USERNAME>           -> ... USERDATA  
                        -p <NOTE|NOTEBOOK>      -> ... PATH
                -c [arg]                        -> change ...
                    arg:
                        -p CURRENTPW NEWPW      -> ...PASSWORD
                        -d OLDPATH NEWPATH      -> ... DOWNLOADPATH
                -d [arg]                        -> download ...
                    arg:
                        -a                      -> ... all
                        ...                     -> ...
                -f <TAG|NOTENAME|NOTEBOOKNAME>  -> find
                -e <NOTE|NOTEBOOK|(USERNAME)>   -> delete
                -s                              -> sync with Cloud
'''

'''
params = ["log", "user"]
param_info = {
    "log": {
        "long": "--log",
        "short": "-l",
        "nargs": "?",
        "const": None,
        "default": "ALL",
        "type": str,
        "choices": None,
        "required": False,
        "help": "Shows the Log-File",
        "metavar": "LOGTYPE"
    },
    "user": {
        "long": "--user",
        "short": "-u",
        "nargs": "1",
        "const": None,
        "default": "ALL",
        "type": str,
        "choices": None,
        "required": False,
        "help": "Shows the Log-File",
        "metavar": "LOGTYPE"
    },

}


class ParsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print self.dest

        print namespace.__dict__[self.dest]

# create the top-level parser
parser = argparse.ArgumentParser(prog="evernote", description="Evernote-CLI")

mutex_group = parser.add_mutually_exclusive_group()
# create Handler for Logging
mutex_group.add_argument("-l", "--log")

toplevel_subparser = parser.add_subparsers(help='commands in comibinition with user')

# create the parser for the "user" command
parser_user = toplevel_subparser.add_parser('user', help='--help')
mutex_group_user = parser_user.add_mutually_exclusive_group()
parser_user.add_argument("username", default="default")
parser_user.add_argument("-t", metavar="TOKEN PASSWD")

seclvl_subparser = parser_user.add_subparsers(help="commands in combi with passwd")
parser_passwd = seclvl_subparser.add_parser("passwd", help="--help")
parser_passwd.add_argument("passwd", nargs=1, metavar="PASSWD")

# parse some argument lists
print parser.parse_args("user -h".split())
#parser.parse_args(['--foo', 'b', '--baz', 'Z'])

'''
'''
# Level_2-Param (token, password) -> user-Group
group_token = group_user.add_mutually_exclusive_group()
group_passwd = group_user.add_mutually_exclusive_group()

# Level_3-Param (visualize, change, download, find, delete, sync) -> passwd-Group
group_visualize = group_passwd.add_mutually_exclusive_group()
group_change = group_passwd.add_mutually_exclusive_group()
group_download = group_passwd.add_mutually_exclusive_group()
# complete group_find, -_delete and -_sync if arguments receive sub-arguments

# add arguments to the appropriate groups
'''
'''
for param in params:
parser.add_argument(param_info[param]["short"],
                    param_info[param]["long"],
                    action=ParsAction,
                    nargs=param_info[param]["nargs"],
                    const=param_info[param]["const"],
                    default=param_info[param]["default"],
                    type=param_info[param]["type"],
                    choices=param_info[param]["choices"],
                    required=param_info[param]["required"],
                    help=param_info[param]["help"],
                    metavar=param_info[param]["metavar"],
                    dest=param )
'''

class Top_Level_Action(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if self.dest == "log":
            logtype = values
            print logtype
            # TODO: Log-Funktion einfuegen
        elif self.dest == "user":
            print values
            user_level_parser = argparse.ArgumentParser(description="EVERNOTE-CLI", prog="evernote ... --user",
                                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                                        prefix_chars=":")
            add_arguments(user_level_parser, user_level_param, user_level_dict)
            mutex_group = user_level_parser.add_mutually_exclusive_group()
            add_arguments(mutex_group, user_level_mutex_param, user_level_mutex_dict)

            # kann entfallen wenn Problem mit Praefix geklaert ist
            if "h" in values:
                print user_level_parser.print_help()
                values.remove("h")

            user_level_parser.parse_args(values)
        else:
            print "Manual"
            pass
            # TODO: print Manual

class User_Level_Action(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        pass

# praefix-> -
top_level_mutex_param = ["log", "user", "man"]
#top_level_param = []
top_level_mutex_dict = {
    "log": {
        "long": "--log",
        "short": "-l",
        "action": Top_Level_Action,
        "nargs": "?",
        "const": None,
        "default": "ALL",
        "type": str,
        "choices": "BWI",  # Ergaenzungen von Logtypen
        "required": False,
        "help": "Shows the Log-File",
        "metavar": "LOGTYPE"
    },
    "user": {
        "long": "--user",
        "short": "-u",
        "action": Top_Level_Action,
        "nargs": "*",
        "const": None,
        "default": None,
        "type": str,
        "choices": None,
        "required": False,
        "help": "type: -u USERNAME h \n...for more information",
        "metavar": "."
    },
    "man": {
        "long": "--man",
        "short": "-m",
        "action": Top_Level_Action,
        "nargs": 0,
        "const": None,
        "default": None,
        "type": None,
        "choices": None,
        "required": False,
        "help": "print Manual",
        "metavar": None
    }
}
#top_level_dict = {}

# praefix -> :
user_level_mutex_param = ["token", "passwd"]
user_level_param = ["user"]
user_level_mutex_dict = {
    "token": {
        "long": "::token",
        "short": ":t",
        "action": User_Level_Action,
        "nargs": None,
        "const": None,
        "default": None,
        "type": str,
        "choices": None,
        "required": False,
        "help": "Create new User",
        "metavar": "TOKEN PASSWD"
    },
    "passwd": {
        "long": "::passwd",
        "short": ":p",
        "action": User_Level_Action,
        "nargs": "?",
        "const": None,
        "default": "John Doe",
        "type": str,
        "choices": None,
        "required": False,
        "help": "need for passwd-commands",
        "metavar": "PASSWD"
    }
}
user_level_dict = {
    "user": {
        "long": "user",
        "short": None,
        "action": User_Level_Action,
        "nargs": "?",
        "const": None,
        "default": "John Doe",
        "type": str,
        "choices": None,
        "required": False,
        "help": None,
        "metavar": "USERNAME"
    }
}

def add_arguments(parser, params, dict):
    for param in params:
        # for optional arguments
        if dict[param]["short"] is not None:
            parser.add_argument(
                dict[param]["short"],
                dict[param]["long"],
                action=dict[param]["action"],
                nargs=dict[param]["nargs"],
                const=dict[param]["const"],
                default=dict[param]["default"],
                type=dict[param]["type"],
                choices=dict[param]["choices"],
                required=dict[param]["required"],
                help=dict[param]["help"],
                metavar=dict[param]["metavar"],
                dest=param
            )
        # for positional arguments
        else:
            parser.add_argument(
                dict[param]["long"],
                action=dict[param]["action"],
                nargs=dict[param]["nargs"],
                const=dict[param]["const"],
                default=dict[param]["default"],
                type=dict[param]["type"],
                choices=dict[param]["choices"],
                help=dict[param]["help"],
                metavar=dict[param]["metavar"]
            )
    return parser

if __name__ == "__main__":
    top_level_parser = argparse.ArgumentParser(description="EVERNOTE-CLI", prog="evernote", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    mutex_group = top_level_parser.add_mutually_exclusive_group()
    add_arguments(mutex_group, top_level_mutex_param, top_level_mutex_dict)
    top_level_parser.parse_args("-u tom :h".split())
