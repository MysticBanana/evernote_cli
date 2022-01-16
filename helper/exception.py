# coding=utf-8
from time import sleep
import traceback
import enum
import traceback
import sys


class EvernoteException(BaseException):
    logger = None
    fun_mode = False

    # if testing / debugging this is True (gets set in .config.json) for more information
    testing = True

    class ErrorReason(enum.Enum):
        DEFAULT = 1

    def __init__(self, error_type=ErrorReason.DEFAULT, desc=None):
        """
        When error gets called generate a custom error description / stack trace and write it to the log and console output
        :param error_type: Enum ErrorReason
        :param desc: closer error description (can be empty empty)
        """
        self.error_type = error_type
        self.description = desc

        self.return_text = "{}: {}{}".format(self.__class__.__name__, self.error_type, ("" if self.description is None else ", {}".format(self.description)))

        # can add special info for debug information
        if self.testing:
            pass

        if self.logger is not None:
            self.logger.error(self.return_text + self.full_stack())

        if self.fun_mode:
            self.trigger_long_error()

    # https://stackoverflow.com/questions/6086976/how-to-get-a-complete-exception-stack-trace-in-python
    def full_stack(self):
        """
        generate the full stack trace of the error
        :return: string of the stack trace
        """
        exc = sys.exc_info()[0]
        stack = traceback.extract_stack()[:-1]

        if exc is not None:
            del stack[-1]

        trc = '"\n"Traceback (most recent call last):\n'
        stack_str = trc + ''.join(traceback.format_list(stack))
        if exc is not None:
            stack_str += '  ' + traceback.format_exc().lstrip(trc)
        return stack_str

    def trigger_long_error(self):
        print "Da kommt ein Error, weißt du was mich das tät?\n"
        sleep(3.5)
        print "\nBelasten!"
        sleep(2)

    def __str__(self):
        return "\nSowwy me errored UwU\n" if self.fun_mode else "" + self.return_text
        #return "{}: {}{}".format(self.__class__.__name__, self.error_type, ("" if self.description is None else ", {}".format(self.description)))

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    # EvernoteException.fun_mode = True
    try:
        0/0
    except Exception as e:
        raise EvernoteException(e, "test reason")
