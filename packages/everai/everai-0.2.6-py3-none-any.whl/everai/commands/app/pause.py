import typing

from everai.app import App
from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction
from everai.app.app_manager import AppManager
from everai.commands.app import add_app_name_to_parser, app_detect


class PauseCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    @app_detect(optional=True)
    def setup(parser: _SubParsersAction, app: typing.Optional[App]):
        pause_parser = parser.add_parser("pause", help="Pause an app, all worker will be stopped")

        add_app_name_to_parser(pause_parser, app, arg_name='name')

        pause_parser.set_defaults(func=PauseCommand)

    @command_error
    def run(self):
        AppManager().pause(self.args.name)
