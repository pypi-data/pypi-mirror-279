from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult


def chained(func):
    def wrapper(instance, *args, **kwargs) -> Cursor | InsertOneResult | dict:
        result: Cursor | InsertOneResult | dict = func(instance, *args, **kwargs)
        if instance.chained:
            instance._result = result if result else {}
            return instance
        else:
            return result

    return wrapper
