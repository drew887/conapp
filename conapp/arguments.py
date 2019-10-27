import argparse
import sys

from conapp.commands import apply, snapshots


def get_args(args: list) -> argparse.Namespace:
    """Build an argparser and return a Namespace"""

    parser = argparse.ArgumentParser(prog='conapp', description='conapp a simple Config Applier')
    parser.set_defaults(command=None)

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Valid commands",
        help="sub-command help",
    )

    apply_group = subparsers.add_parser(apply.COMMAND, help="apply a config")
    snapshot_group = subparsers.add_parser(snapshots.COMMAND, help="manage snapshots")

    apply.setup_arguments(apply_group)
    snapshots.setup_arguments(snapshot_group)
    # TODO: Add other commands

    args = parser.parse_args(args=args)

    if args.command is None:
        parser.print_usage()
        sys.exit(1)
    else:
        return args
