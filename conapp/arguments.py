import argparse

from conapp.definitions import *


def validate_apply(args: argparse.Namespace) -> bool:
    if args.user is None:
        print("Error, apply requires a user to be passed")
        return False

    return True


APPLY_COMMAND = 'apply'

COMMANDS = {
    APPLY_COMMAND: validate_apply,
    # 'track': 2,
    # 'commit': 3,
    # 'checkout': 4
}


def validate_args(args: argparse.Namespace) -> bool:
    command = COMMANDS.get(args.command, None)

    if command is None:
        print(
            "Error command must be one of: \n" +
            ' '.join(COMMANDS.keys())
        )
        return False

    return command(args)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='conapp a simple Config Applier')
    parser.set_defaults(command=None)

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Valid commands",
        help="sub-command help",
    )

    apply_group = subparsers.add_parser(APPLY_COMMAND, help="apply a config")
    apply_group.set_defaults(command=APPLY_COMMAND)
    apply_group.add_argument(
        '-u',
        '--user',
        required=True,
        help='username to pull from'
    )
    apply_group.add_argument(
        '-r',
        '--repo',
        default='config',
        help='repo name to pull, defaults to config'
    )
    apply_group.add_argument(
        '--no-download',
        action='store_true',
        help='Use already downloaded copy'
    )
    apply_group.add_argument(
        '-b',
        '--bitbucket',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.BITBUCKET,
        help='pull from bitbucket'
    )
    apply_group.add_argument(
        '-g',
        '--github',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.GITHUB,
        help='pull from bitbucket'
    )

    return parser.parse_args()
