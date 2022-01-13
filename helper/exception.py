# coding=utf-8
from time import sleep
import traceback
import enum


class EvernoteException(BaseException):
    logger = None
    fun_mode = False

    class ErrorReason(enum.Enum):
        DEFAULT = 1


    def __init__(self, error_type, desc = None):
        # todo print full stacktrace
        self.error_type = error_type
        self.description = desc
        self.error_text = "{}: {}{}".format(self.__class__.__name__, self.error_type, ("" if self.description is None else ", {}".format(self.description)))

        if self.logger is not None:
            self.logger.error(self.error_text)

        if self.fun_mode:
            print "Da kommt ein Error, weißt du was mich das tät?\n"
            sleep(3.5)
            print "\nBelasten!"
            sleep(2)

    def __str__(self):
        return "\nSowwy me errored UwU\n" + self.error_text
        #return "{}: {}{}".format(self.__class__.__name__, self.error_type, ("" if self.description is None else ", {}".format(self.description)))

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    # EvernoteException.fun_mode = True
    try:
        0/0
    except Exception as e:
        raise e(EvernoteException.ErrorReason.DEFAULT, "test reason")
