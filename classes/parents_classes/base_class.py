from typing import Dict, Any, List, Callable

def debug_logger(func: Callable):
    def wrapper(cls, **kwargs: Dict[str, Any]):
        msg = "set_cls_params: class = %s , params = %s" % ()
        print(msg)

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