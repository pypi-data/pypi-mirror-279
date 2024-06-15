from functools import wraps
from typing import get_type_hints


class Injector:
    type_kwargs = {}

    @staticmethod
    def register(type_, **kwargs):
        Injector.type_kwargs[type_.__name__] = kwargs

    @staticmethod
    def get_instance(type_):
        kwargs = Injector.type_kwargs.get(type_.__name__, {})
        return type_(**kwargs)


def inject(method):
    @wraps(method)
    def wrapper(self, **kwargs):
        type_name = type(self).__name__
        kwargs = Injector.type_kwargs.get(type_name, {}) | kwargs
        type_hints = get_type_hints(method)
        type_hints.pop("return", None)

        for param, type_ in type_hints.items():
            instance = kwargs.get(param)

            if instance is None:
                instance = Injector.get_instance(type_)

            kwargs[param] = instance

        return method(self, **kwargs)

    return wrapper

