import enum

class EvernoteException(BaseException):
    logger = None

    class ErrorReason(enum.Enum):
        DEFAULT = 1


    def __init__(self, error_type, desc = None):
        self.error_type = error_type
        self.description = desc
        self.error_text = "{}: {}{}".format(self.__class__.__name__, self.error_type, ("" if self.description is None else ", {}".format(self.description)))

        if self.logger is not None:
            self.logger.error(self.error_text)

    def __str__(self):
        return "\n" + self.error_text
        #return "{}: {}{}".format(self.__class__.__name__, self.error_type, ("" if self.description is None else ", {}".format(self.description)))

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    raise EvernoteException(EvernoteException.ErrorReason.DEFAULT, "test reason")