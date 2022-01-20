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

    def get_user_input(self, text):
        """
        If you need a request from user yes/no use this
        """

        # check for multiple different inputs by user
        decision = {
            "yes": ["yes", "y", "true", "yee", "yes i want"],
            "no": ["no", "n", "nope", "shut up", "false", ""]
        }

        max_wrong_input = 3
        input_counter = 0
        while input_counter < max_wrong_input:
            # py 2 require raw_input
            reply = raw_input("{text} (yes|no) [default=no]: ".format(text=text))

            if reply in decision["yes"]:
                return True
            elif reply in decision["no"]:
                return False
            print "Type 'yes' or 'no' please \n After {} using default=no or try parameter --force".format(max_wrong_input-input_counter)

            input_counter += 1

        return False

    def print_help(self, command=None):

        usage = self.get_usage_command(command)

        # used to create usage strings
        optional = "[%s]"
        user_input = "<{}>"
        exclusive = "({})"
        _exclusive = " | "

        output = "Usage: $%s" % self.controller.NAME
        if command is not None:
            for i in usage:
                output += " " + i[0][0]
                if type(i[1]) == str:
                    output = i[1] + ":\n" + output

                    if type(i[2]) == dict:
                        # todo mit <>
                        output += " " + exclusive.format(_exclusive.join(i[2].keys()))
                    continue

                if len(i) > 1:
                    for para in i[1]:
                        output += " " + user_input.format((para if i[1][para] else optional % para))

            print output + "\n"
        else:
            print output + usage + "\n"


        for i in self.get_help_tree(command=command):
            print i

    def get_help_tree(self, ret_dict=None, tab_counter=0, command=None):
        """
        Returns a tree dict starting from root or from "command" parameter in the origin tree
        :param ret_dict: recursive dict to return
        :param tab_counter: add tab / space character to the string and counting the depth
        :param command: if none returns the complete dict as a string, if name of a parameter returns a dict tree starting there
        :return:
        """
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
        """
        creates a usage string based on the parameter tree. If none returns the default string, if not returns usage
        from the parameter with all required parameters
        """

        usage = ""
        usage_param = []

        if command is None:
            usage = "[-h] [-u <username> (-n [<token>] <password> | -p <password>) --command] "
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

if __name__ == "__main__":
    pass