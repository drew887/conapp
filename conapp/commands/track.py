import os
import argparse
import subprocess
import shutil

from conapp.file_paths import CONFIG_TRACK_DIR
from conapp.validate import validate_subprocess
from conapp.url_generators import CHECKOUT_RESOLVERS
from conapp.definitions import Hosts

COMMAND = "local"
COMMAND_HELP = "Command for managing a local repo"

TRACK_REPO_FOLDER_NAME = 'repo'


def setup_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(command=lambda x: parser.print_usage())

    sub_parser = parser.add_subparsers()

    checkout_parser = sub_parser.add_parser(
        "checkout",
        help="checkout a bare repo"
    )
    checkout_parser.set_defaults(command=checkout_command)

    checkout_parser.add_argument(
        '-u',
        '--user',
        required=True,
        help='username to pull from'
    )
    checkout_parser.add_argument(
        '-r',
        '--repo',
        default='config',
        help='repo name to pull, defaults to config'
    )
    checkout_parser.add_argument(
        '-b',
        '--bitbucket',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.BITBUCKET,
        help='pull from bitbucket'
    )
    checkout_parser.add_argument(
        '-g',
        '--github',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.GITHUB,
        help='pull from bitbucket'
    )

    return parser


def checkout_command(args: argparse.Namespace) -> None:
    """
    Checkout a "bare" repo for local setup
    :param args:
    :return:
    """
    repo_folder = os.path.join(CONFIG_TRACK_DIR, TRACK_REPO_FOLDER_NAME)

    if os.path.exists(repo_folder):
        if input("Repo folder is not empty, delete to continue? [y/N]:").lower() == "y":
            shutil.rmtree(repo_folder, True)
        else:
            print(f"Repo dir not empty, aborting.\nRepo dir = {repo_folder}")
            return

    command = [
        'git',
        'clone',
        '--bare',
        CHECKOUT_RESOLVERS.get(args.host)(args.user, args.repo),
        repo_folder,
    ]

    print(f"about to execute '{' '.join(command)}'")

    if input("Proceed [y/N]? ").lower() == "y":
        validate_subprocess(
            subprocess.run(command)
        )
        # TODO: Add output of what to do next (ie call `conapp local env`) to
        #  setup local stuff. Need to do more than bash eventually

    pass
