import functools
import typing
from argparse import ArgumentParser

from everai.app import App
from everai.runner import find_target


def add_app_name_to_parser(parser: ArgumentParser,
                           app: typing.Optional[App],
                           arg_name: str = 'app_name'):
    if app is not None:
        parser.add_argument(arg_name, help='The app name', type=str, nargs='?', default=app.name)
    else:
        parser.add_argument(arg_name, help='The app name', type=str)


def app_detect(optional: bool = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            app = find_target(target_type=App)
            if not optional and app is None:
                raise Exception('No app found in app.py')
            return func(app=app, *args, **kwargs)

        return wrapper
    return decorator


def app_name(optional: bool = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            app = find_target(target_type=App)
            if not optional and app is None:
                raise Exception('No app found in app.py')

            return func(name=app.name, *args, **kwargs)

        return wrapper
    return decorator
