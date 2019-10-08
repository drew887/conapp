import argparse

from swat.definitions import *


def validate_apply(args: argparse.Namespace) -> bool:
    if args.user is None:
        print("Error, apply requires a user to be passed")
        return False

    return True


COMMANDS = {
    'apply': validate_apply,
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
    parser = argparse.ArgumentParser(description='a Shitty Wrapper Around Tar')

    parser.add_argument(
        '-u',
        '--user',
        help='username to pull from'
    )
    parser.add_argument(
        '-r',
        '--repo',
        default='config',
        help='repo name to pull, defaults to config'
    )
    parser.add_argument(
        '-b',
        '--bitbucket',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.BITBUCKET,
        help='pull from bitbucket'
    )
    parser.add_argument(
        '-g',
        '--github',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.GITHUB,
        help='pull from bitbucket'
    )
    parser.add_argument(
        'command',
        nargs='?'
    )

    return parser.parse_args()
