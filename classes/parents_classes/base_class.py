from typing import Dict, Any, List, Callable

from logging import getLogger

logger = getLogger(__name__)

def debug_logger_inst(func: Callable):
    ''' Debug logger for init method '''
    def wrapper(self, **kwargs: Dict[str, Any]):
        msg = "debug_logger_init: class=%s, params=%s" % \
            (self.__class__.__name__, str(kwargs))
        logger.debug(msg)

        return func(self, **kwargs)

    return wrapper

def debug_logger(func: Callable):
    ''' Debug logger for classmethod '''
    def wrapper(cls, **kwargs: Dict[str, Any]):
        msg = "debug_logger_classmethod: class=%s, params=%s" % \
            (cls.__name__, str(kwargs))
        logger.debug(msg)

        return func(cls, **kwargs)

    return wrapper

class BaseClass:
    # list cls param
    parameters: List[str] = []

    @classmethod
    @debug_logger
    def set_cls_params(cls, **params: Dict[str, Any]):
        ''' Set static class parameters '''
        for key in cls.parameters:
            setattr(cls, key, params[key])

        return 0

if __name__ == "__main__":
    # example
    test = {"a": 1, "b": 2}
    BaseClass.parameters = ["a", "b"]
    BaseClass.set_cls_params(**test)