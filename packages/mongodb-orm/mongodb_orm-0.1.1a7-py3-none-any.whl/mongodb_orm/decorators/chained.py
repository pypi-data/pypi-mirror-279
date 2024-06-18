from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult
from typing import Union


def chained(func):
    def wrapper(instance, *args, **kwargs) -> Union[Cursor, InsertOneResult, dict]:
        result: Union[Cursor, InsertOneResult, dict] = func(instance, *args, **kwargs)
        if instance.chained:
            instance._result = result if result else {}
            return instance
        else:
            return result

    return wrapper
