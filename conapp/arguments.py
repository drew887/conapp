import argparse

# from conapp.definitions import Hosts
from conapp.commands import apply


COMMANDS = {
    apply.COMMAND: apply.validate,
    # 'track': 2,
    # 'commit': 3,
    # 'checkout': 4
}


def validate_args(args: argparse.Namespace) -> bool:
    """Validate passed arguments; deprecated thanks to argparse"""
    command = COMMANDS.get(args.command, None)

    if command is None:
        print(
            "Error command must be one of: \n" +
            ' '.join(COMMANDS.keys())
        )
        return False

    return command(args)


def get_args() -> argparse.Namespace:
    """Build an argparser and return a Namespace"""

    parser = argparse.ArgumentParser(description='conapp a simple Config Applier')
    parser.set_defaults(command=None)

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Valid commands",
        help="sub-command help",
    )

    apply_group = subparsers.add_parser(apply.COMMAND, help="apply a config")

    apply.setup_arguments(apply_group)
    # TODO: Add other commands

    return parser.parse_args()
