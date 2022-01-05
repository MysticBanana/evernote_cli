import enum
import param_loader_2


class DisplayManager:
    def __init__(self, controller):
        self.controller = controller
        self.logger = controller.create_logger("Display")

        self.tab_size = "   "

    def default_display(self, display_text):
        self.logger.debug(display_text)

    def default_error(self, reason):
        self.logger.error(reason)
        raise EvernoteException (reason)

    def display_dict(self, data):
        # dictionary displayed: "-u --user              help text zu -u"
        pass

    def get_dict(self, arg="-h"):
        self.help_dict = param_loader_2.ArgumentParser.args_dict

    def print_help(self, ret_dict=None, tab_counter=0):
        ret_dict = ret_dict if ret_dict else param_loader_2.ArgumentParser.args_dict

        for k, v in ret_dict.items():

            if type(v) == dict:
                if "opt_str" in v:
                    string = "{tabs}{opt_str} <{metavar}> {helptext}".format(opt_str=v["opt_str"],
                                                                             metavar=v["metavar"], helptext=v["help"],
                                                                             tabs=(self.tab_size * tab_counter))
                    print(string)
                else:
                    self.print_help(v, tab_counter + 1)

class EvernoteException(BaseException):
    class Exceptions(enum.Enum):
        pass


if __name__ == "__main__":
    pass