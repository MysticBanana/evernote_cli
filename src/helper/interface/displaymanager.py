# coding=utf-8

import enum
import argument_parser
import arg_config


class HelpMenu:
    _usage_str = ""
    _description = ""
    _option_str = ""

    # todo
    _name = "evernote_cli.py"

    def __init__(self):
        pass

    def __str__(self):
        return "Usage: {}\n\n" \
               "{:<5}\n\n" \
               "Commands\n" \
               "{:<5}".format(self._usage_str, self._description, self._option_str)


class DisplayManager:
    def __init__(self, controller):
        self.controller = controller
        self.logger = controller.create_logger("Display")

        self.help_dict = argument_parser.ArgumentParser.commands

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
            "yes": ["yes", "y", "true", "yee", "yes i want", "ja"],
            "no": ["no", "n", "nope", "shut up", "false", "", "nein"]
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
            print "Type 'yes' or 'no' please \n After {} using default=no or try parameter --force".format(
                max_wrong_input - input_counter)

            input_counter += 1

        return False

    def print_help(self, command=None):
        pm = argument_parser.ArgumentParser.parameter_structure
        help_string = pm.get_final_output(command)
        print help_string


class UserError(enum.Enum):
    TOO_MANY_ARGUMENT = 1
    TOO_FEW_ARGUMENT = 2
    MISSING_ARGUMENT = 3
    MISSING_PARAMETER = 4
    AUTHENTICATION_FAILED = 5
    FALSE_PARAMETER = 6
    FALSE_ENCRYPTION_LEVEL = 7


error = {
    UserError.TOO_MANY_ARGUMENT: "Too many arguments! Expected at most 8 arguments, got <rep>",  # not used atm
    UserError.TOO_FEW_ARGUMENT: "Too few arguments! At least one argument expected",
    UserError.MISSING_ARGUMENT: "At least one argument is missing!",
    UserError.MISSING_PARAMETER: "Parameter is missing!",
    UserError.AUTHENTICATION_FAILED: "Authentication failed!"
                                     " Check if password and username are correct."
                                     " If you are using the program for the first time, create a new user with:"
                                     "    '-u <username> -n <passwd>' "
                                     " Tried [<rep>, <rep>]",
    UserError.FALSE_PARAMETER: "The parameter is incorrect! Parameter <rep> does not exist in this context",
    UserError.FALSE_ENCRYPTION_LEVEL: "Incorrect encryption level! Expected level 0 to <rep>, got <rep>"
}

if __name__ == "__main__":
    pass