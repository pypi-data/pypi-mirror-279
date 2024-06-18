import argparse
import typing
from argparse import _SubParsersAction

from everai.app import App
from everai.app.app_manager import AppManager
from everai.commands.command import command_error, ClientCommand

from everai.commands.app import app_detect, add_app_name_to_parser


class DeleteCommand(ClientCommand):
    parser: _SubParsersAction = None

    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        delete_parser = parser.add_parser(
            "delete",
            help="Delete an app",
            description='Delete an app from manifest file or an App object in app.py. \n'
                        '--from-file indicates a manifest file for create app, \n'
                        'otherwise, everai command line tool find app setup in app.py',
            formatter_class=argparse.RawTextHelpFormatter,
        )
        delete_parser.add_argument('--force', action='store_true')

        file_group = delete_parser.add_argument_group('from file')
        file_group.add_argument(
            '-f',
            '--from-file',
            type=str,
            help='Delete app from manifest file (format in yaml), for example: --from-file filename'
        )

        delete_parser.set_defaults(func=DeleteCommand)
        DeleteCommand.parser = delete_parser

    @command_error
    @app_detect(optional=True)
    def run(self, app: typing.Optional[App]):
        if self.args.from_file is not None:
            app = App.from_yaml_file(self.args.from_file)
        else:
            if app is None:
                DeleteCommand.parser.error('could not found App object in app.py')

        name = app.name
        if not self.args.force:
            ret = input('\n[*] Deleting an app is really dangerous, are you sure[y/N]')
            if ret not in ['y', "Y"]:
                print('user canceled')
                return

        AppManager().delete(name)

        print(f"App `{name}` deleted")
