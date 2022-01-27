import functools
from helper import exception


def exception_handler(error=exception.EvernoteException, desc="", error_reason=None, stop=True):
    """
    Exception handler to catch exception from functions. Calls the error given or default EvernoteException
    :param error: Can be a custom Error inheriting from Exception
    :param desc: Description of the error
    :param error_reason: Enum for custom error
    :param stop: If error should be ignored or raised
    """
    def decorator(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if stop:
                    raise error(error_reason or e, desc)

        return inner
    return decorator