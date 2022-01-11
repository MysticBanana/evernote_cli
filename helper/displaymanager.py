import enum
import param_loader_2


class DisplayManager:
    def __init__(self, controller):
        self.controller = controller
        self.logger = controller.create_logger("Display")

        self.help_dict = param_loader_2.ArgumentParser.args_dict

        self.tab_size = "  "
        self.max_tabs = 5

        # todo fehleingabe text als dict/liste mit enum zum zugreifen

    def default_display(self, display_text):
        self.logger.debug(display_text)

    def default_error(self, reason):
        self.logger.error(reason)
        raise EvernoteException (reason)

    def display_dict(self, data):
        # dictionary displayed: "-u --user              help text zu -u"
        pass

    def print_help(self, command=None):
        usage = self.get_usage_command(command)
        optional = "[%s]"
        user_input = "<{}>"
        exclusive = "({})"
        _exclusive = " | "

        # todo evernote name
        output = "Usage: $%s" % "evenote"
        for i in usage:
            output += " " + i[0][0]
            if type(i[1]) == str:
                output = i[1] + ":\n" + output

                if type(i[2]) == dict:
                    output += " " + exclusive.format(_exclusive.join(i[2].values()))
                continue

            if len(i) > 1:
                for para in i[1]:
                    output += " " + user_input.format((para if i[1][para] else optional % para))

        print output + "\n"

        for i in self.get_help_tree(command=command):
            print i



    def get_help_tree(self, ret_dict=None, tab_counter=0, command=None):
        ret_dict = ret_dict if ret_dict else self.help_dict
        lines = []

        for k, v in ret_dict.items():
            if type(v) == dict:
                if "opt_str" in v:
                    if "help" not in v:
                        continue

                    tabs = "\t"*(5-tab_counter)
                    if command: tab_counter = 0
                    string = "{spaces}{opt_str} | {opt_str_long} {tabs} {helptext}".format(opt_str=v["opt_str"][0],
                                                                                    opt_str_long=v["opt_str"][1],
                                                                                    helptext=v["help"],
                                                                                    spaces=(self.tab_size * tab_counter),
                                                                                           tabs=tabs)

                    ret = self.get_help_tree(v, tab_counter + 1, command)
                    if command is None or command in v["opt_str"]:
                        ret.insert(0, string)

                    lines.append(ret)

        return [i for row in lines for i in row]

    def get_usage_command(self,command=None, ret_dict=None):
        usage = ""
        usage_param = []

        if command is None:
            # todo: define a var that holds the programm name!!
            program_name = "evernote"
            usage = "$ %s [-h] [-u <username> (-n [<token>] <password> | -p <password>) --command] " % program_name

            return usage

        ret_dict = ret_dict if ret_dict else self.help_dict

        for k, v in ret_dict.items():
            if type(v) == dict:
                if ("opt_str" in v):
                    if (command in v["opt_str"]):
                        # maybe find a better way for new features
                        require = v["require"]
                        if len(v["require"]) == 0:
                            pass

                            for i in list(v):
                                j = v[i]
                                if "opt_str" in j:
                                    require[i] = j["opt_str"][0]

                        usage_param.append((v["opt_str"], k, require))
                        # usage_param.append((require,))
                        break
                    else:
                        ret = self.get_usage_command(command, v)
                        if len(ret) > 0:
                            ret.insert(0, (v["opt_str"], v["require"]))
                            usage_param = ret

        return usage_param


class EvernoteException(BaseException):
    class Exceptions(enum.Enum):
        pass


if __name__ == "__main__":
    pass