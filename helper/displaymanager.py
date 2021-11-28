import enum
import param_loader_2

class DisplayManager:
    def __init__(self, controller):
        self.controller = controller
        self.logger = controller.create_logger("Display")

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






class EvernoteException(BaseException):
    class Exceptions(enum.Enum):
        pass



if __name__ == "__main__":
    pass