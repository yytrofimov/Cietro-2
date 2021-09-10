import inspect
import sys

sys.path.insert(0, '../')
import exceptions as e


def check_types(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        func_signature = str(inspect.signature(func)).strip('()')
        args_order = list(_.split(': ')[0] for _ in func_signature.split(', '))
        for arg_key, arg in zip(args_order, args):
            kwargs[arg_key] = arg
        annotations = func.__annotations__
        defaults_kwargs = func.__defaults__
        defaults = {}
        if defaults_kwargs:
            for key, kwarg in zip(reversed(args_order), defaults_kwargs):
                defaults[key] = kwarg
        for key, kwarg in kwargs.items():
            if key in annotations and (
                    key in defaults and kwarg != defaults[key] or key not in defaults) and not isinstance(kwarg,
                                                                                                          annotations[
                                                                                                              key]):
                raise e.WrongType(
                    '{} arg should be instance of {}. Given value: {} is instance of {}'.format(key,
                                                                                                annotations[
                                                                                                    key],
                                                                                                kwarg,
                                                                                                type(kwarg)))
        return func(**kwargs)

    return wrapper
