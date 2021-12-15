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

test_arguments = {
    "passwd":
        {
            "opt_str": ["passwd"],
            "nargs": 1,
            "type": str,
            "help": "Your self chosen password for the Evernote CLI"
        },
    "test": "hallo"
}


def cmd1(args):
    print "cmd1 print ...", args


def cmd2(args):
    print "cmd2 print ...", args


class Test(argparse.Action):
    def __call__(self, *args, **kwargs):
        print "TEST"


class ArgParser():
    def __init__(self, arg_string, arg_dict, main_class=None, *args,
                 **kwargs):  # TODO: muesste auch mit kwargs funktionieren
        global_parser = argparse.ArgumentParser(description="EVERNOTE-CLI",
                                                prog="evernote",
                                                formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                                )
        global_parser.add_argument(*arg_dict["passwd"]["opt_str"],
                                   **{key: val for key, val in arg_dict["passwd"].items() if key != 'opt_str'})

        parser = argparse.ArgumentParser(prog="Prog")

        subparsers = parser.add_subparsers(dest="cmd")
        parserCmd1 = subparsers.add_parser("cmd1", help="First Command")
        parserCmd1.set_defaults(func=cmd1)
        parserCmd2 = subparsers.add_parser("cmd2", help="Second Command")
        parserCmd2.set_defaults(func=cmd2)

        a = "123".split()
        args, extras = global_parser.parse_known_args(a)
        if len(extras) > 0 and extras[0] in ["cmd1", "cmd2"]:
            args = parser.parse_args(extras, namespace=args)
            args.func(args)
        else:
            print "doing system with", args, extras

    def __call__(self, *args, **kwargs):
        pass


def default(parser):
    print "Test"
    parser.print_help()


''' 
Module fuer ...
    "pos_arg_name":
        {
            "subparser": False,
            "opt_str": [],
            "action": None,
            "nargs": None,
            "const": None,
            "default": None,
            "type": None,
            "choices": None,
            "help": None,
            "metavar": None
        }
    "opt_arg_name":
        {
            "subparser": False,
            "opt_str": [],
            "action": None,
            "nargs": None,
            "const": None,
            "default": None,
            "type": None,
            "choices": None,
            "required": None,
            "help": None,
            "metavar": None,
            "dest": None
        }
    "subparser":
        {
            "subparser": True,
            "help": None,
            # weiterer args oder subparser
        }
}
'''

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
                    "action": Test,
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
                            "action": Test,
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
                                    "action": Test,
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


def create_old(args_dict, subparsers, trenner):
    trenner += "\t"
    for i in args_dict:
        if i == "subparser":
            continue
        if args_dict[i]["subparser"]:
            subparser = parser.add_parser(i, args_dict[i]["help"])

            print trenner, "create subparser ", i, " in ", parser
            create(args_dict[i], subparser, trenner)
        elif args_dict[i]["subparser"] == False:
            parser.add_argument(*args_dict[i]["opt_str"],
                                **{key: val for key, val in args_dict["passwd"].items() if
                                   key != 'opt_str' or key != 'subparser'})
            print trenner, "create argument", i, " in ", parser
    return parser


if __name__ == "__main__":
    def create(args_dict, subparsers, parser):
        for i in args_dict:
            if i in ["subparser", "default", "help"]:
                continue
            if args_dict[i]["subparser"]:
                pars = subparsers.add_parser(i, help=args_dict[i]["help"])
                subpars = pars.add_subparsers(dest=i)
                #if args_dict[i]["default"]:
                #    pars.set_defaults(func=args_dict[i]["default"])
                create(args_dict[i], subpars, pars)
            elif args_dict[i]["subparser"] == False:
                parser.add_argument(*args_dict[i]["opt_str"],
                                    **{key: val for key, val in args_dict[i].items() if key not in ["opt_str", "subparser"]})
                #parser.add_argument(*arguments["user"]["username"]["opt_str"],
                #        **{key: val for key, val in arguments["user"]["username"].items() if key not in ["opt_str", "subparser"]})
        return parser

    '''
    parser = argparse.ArgumentParser(prog="evernote")
    subparsers_global = parser.add_subparsers(dest="global")
    parser_user = subparsers_global.add_parser("user", help=arguments["user"]["help"])
    parser_user.add_argument("username", nargs="?",default="John Doe")
    subparsers_user = parser_user.add_subparsers(dest="user")
    subparsers_user.add_parser("token", help="token -h")
    '''
    parser = argparse.ArgumentParser(prog="evernote")
    subparsers = parser.add_subparsers(dest="global")
    parser = create(arguments, subparsers, parser)
    parser.parse_args("user passwd -h".split())
    # a = ArgParser("n", test_arguments)