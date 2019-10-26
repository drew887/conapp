import argparse

from conapp.commands import apply


COMMAND_VALIDATORS = {
    apply.COMMAND: apply.validate,
    # 'track': 2,
    # 'commit': 3,
    # 'checkout': 4
}

COMMANDS = {
    apply.COMMAND: apply.main
}


def validate_args(args: argparse.Namespace) -> bool:
    """Validate passed arguments; deprecated thanks to argparse"""
    validator = COMMAND_VALIDATORS.get(args.command, None)

    if validator is None:
        print(
            "Error command must be one of: \n" +
            ' '.join(COMMAND_VALIDATORS.keys())
        )
        return False

    return validator(args)


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
