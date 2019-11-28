import os
import argparse
import subprocess

from conapp.file_paths import CONFIG_TRACK_DIR
from conapp.validate import validate_subprocess
from conapp.url_generators import CHECKOUT_RESOLVERS
from conapp.definitions import Hosts

COMMAND = "local"
COMMAND_HELP = "Command for managing a local repo"


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
    command = [
        'git',
        'clone',
        '--bare',
        CHECKOUT_RESOLVERS.get(args.host)(args.user, args.repo),
        os.path.join(
            CONFIG_TRACK_DIR,
            "track"
        ),
    ]

    print(f"about to execute '{' '.join(command)}'")

    if input("Precede [y/N]? ") == "y":
        validate_subprocess(
            subprocess.run(command)
        )
        # TODO: Add output of what to do next (ie call `conapp local env`) to
        #  setup local stuff. Need to do more than bash eventually

    pass
