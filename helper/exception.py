import enum

class EvernoteException(BaseException):

    class ErrorType(enum.Enum):
        DEFAULT = 1

    def __init__(self, error_type, desc = None):
        self.error_type = error_type
        self.description = desc

    def __str__(self):
        return "{}: {}{}".format(self.__class__.__name__, self.error_type, ("" if self.description is None else ", {}".format(self.description)))

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    raise EvernoteException(EvernoteException.ErrorType.DEFAULT, "test reason")