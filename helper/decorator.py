import functools
from helper import exception

# https://stackoverflow.com/questions/18327014/how-to-catch-an-exception-in-a-decorator


def exception_handler(error=exception.EvernoteException, desc="", error_reason=None, stop=True):
    def decorator(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise error(error_reason or e, desc)

        return inner
    return decorator