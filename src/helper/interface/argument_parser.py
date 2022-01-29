# coding=utf-8
import helper.krypto_manager
import copy
import helper.interface.displaymanager
import arg_config

'''
$ evernote ...
    -h | --help
    -u | -- user <Username> ...
        -n | --new <Passwd> [<Token>]
        -p | --passwd <Passwd> ...
            -c | --change ...
                -p | --passwd <New_Passwd> [-f]
                -d | --downloadpath <New_path> [-f]
                -e | --encrypt <New encrypion lvl> [-f]
            -d | --download [-f] [<Overwrite>] [<Encryption_Lvl>]
            -e | --encrypt [<Encryption_Lvl>]
            -de | --decrypt
            -rm | --remove
'''


class ArgumentParser:

    parameter_structure = arg_config.ParameterStructure(parameter=arg_config.commands)
    commands = parameter_structure.parameter

    optionals = ["-f", "-o"]

    # for generating help menu
    optional_params = [""]

    def __init__(self, controller, args):
        self.controller = controller

        self.arg_list = args
        self.params = {}
        self.logger = controller.create_logger("argument_parser")

        self.wrong_input = False

    def error(self, msg):
        self.params = {"func": "error", "err_typ": msg}

    def add_input_check_error(self, input_typ, arguments=[]):
        if not self.wrong_input:
            self.wrong_input = True
            self.params = {"func": "input_error", "err_types": []}
        for i in arguments:
            input_typ = input_typ.replace("<rep>", i, 1)
        self.logger.error(input_typ)
        self.params["err_types"].append(input_typ)

    def warning(self, msg):
        self.logger.warning(msg)
        print (msg)

    def get_next_params(self, arguments):
        next_params, next_arg = None, None
        param = self.arg_list.pop(0)
        end = True
        correct_param = False
        for key, _ in arguments.items():
            if param in arguments[key]["opt_str"]:
                correct_param = True
                next_params = arguments[key].get("subcommand")
                if not arguments[key]["func_name"] is None:
                    self.params["func"] = arguments[key]["func_name"]
                else:
                    end = False
                if key == "help":
                    self.params["command"] = []
                    while len(self.arg_list) != 0:
                        self.params["command"].append(self.arg_list.pop(0))
                elif not arguments[key].get("requires") is None:
                    if "none_opt" in arguments[key].get("requires", ""):
                        self.get_args(arguments[key]["requires"]["none_opt"])
                    if "opt" in arguments[key].get("requires", ""):
                        self.get_opt_args(arguments[key]["requires"]["opt"])
        if not correct_param:
            if param in self.optionals:
                return arguments, False
            else:
                self.add_input_check_error(
                    helper.interface.displaymanager.error[helper.interface.displaymanager.UserError.FALSE_PARAMETER], [param])
                return None, True
        return next_params, end

    def get_args(self, args):
        try:
            for arg in args:
                while self.arg_list[0] in self.optionals:
                    self.arg_list.pop(0)
                if len(self.arg_list) == 0:
                    self.add_input_check_error(
                        helper.interface.displaymanager.error[
                            helper.interface.displaymanager.UserError.MISSING_PARAMETER])
                    break
                if type(arg) == tuple:
                    try:
                        self.params[arg[0]] = int(self.arg_list.pop(0))
                    except:
                        self.params[arg[0]] = -1
                    continue
                self.params[arg] = self.arg_list.pop(0)
        except:
            self.add_input_check_error(
                helper.interface.displaymanager.error[helper.interface.displaymanager.UserError.MISSING_PARAMETER])


    def get_opt_args(self, opt_args):
        for arg, typ in opt_args:
            # z.B. arg = "param"; typ = int
            if type(typ) == type:
                try:
                    self.params[arg] = typ(self.arg_list[0])
                    self.arg_list.pop(0)
                except Exception:
                    self.params[arg] = None
            # z.B. arg = "param"; typ = "-f"
            elif type(typ) == list:
                if len(self.arg_list) == 0:
                    self.params[arg] = False
                    continue
                if self.arg_list[0] in typ:
                    self.params[arg] = True
                    self.arg_list.pop(0)
                else:
                    self.params[arg] = False

    def parser(self):
        nr_of_args = len(self.arg_list)
        # Check general number of parameters
        if nr_of_args == 0:
            self.params = {"func": "help", "command": []}
            return
        end = False
        next_param = self.commands

        while not end:
            if len(self.arg_list) == 0:
                self.add_input_check_error(
                    helper.interface.displaymanager.error[helper.interface.displaymanager.UserError.MISSING_ARGUMENT])
                break
            next_param, end = self.get_next_params(next_param)

        if not self.params["func"] in ["version", "help", "error", "input_error"]:
            # add password hash to self.params
            self.params["password_hash"] = helper.krypto_manager.hash_str(self.params["password"])
            check = self.controller.global_data_manager.check_user_hash(self.params["username"],
                                                                        self.params["password_hash"])
            user_exists = self.controller.global_data_manager.is_user(self.params["username"])
            if not self.params["func"] in ["new_user"]:
                # User Input Check
                params = copy.deepcopy(self.params)
                # Check if login data are correct
                if not check:
                    #Authentication failed
                    self.add_input_check_error(
                        helper.interface.displaymanager.error[
                            helper.interface.displaymanager.UserError.AUTHENTICATION_FAILED],
                            [self.params["username"], self.params["password"]])
                for key, val in params.items():
                    if key == "encrypt_lvl" or key == "new_encrypt_lvl":
                        print val
                        print self.controller.max_encryption_level
                        if not val == None:
                            if not 0 <= val <= self.controller.max_encryption_level:
                                # False Encryption Level selected
                                self.add_input_check_error(
                                    helper.interface.displaymanager.error[
                                        helper.interface.displaymanager.UserError.FALSE_ENCRYPTION_LEVEL],
                                    [str(self.controller.max_encryption_level), str(val)])
            else:
                if user_exists:
                    self.params["token"] = -1
                    self.warning("{} exists".format(self.params["username"]))

        if not len(self.arg_list) == 0:
            self.warning("Warning! {} was ignored".format(self.arg_list))
