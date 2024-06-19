import inspect
from collections import OrderedDict


class Utility:
    @staticmethod
    def dict_to_string(dictionary, separator=','):
        return separator.join([f'{k}={v}' for k, v in dictionary.items()])

    @staticmethod
    def map_arg_to_value(function, *args, **kwargs):
        signature = inspect.signature(function)
        params = OrderedDict([(p.name, p.default) for p in signature.parameters.values()])

        for arg_value, param in zip(args, params):
            params[param] = arg_value

        params.update(kwargs)
        return params
