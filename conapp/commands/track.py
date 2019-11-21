import os
import argparse

COMMAND = "track"
COMMAND_HELP = "Command for managing a local repo in the format that conapp expects"


def setup_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(command=lambda x: parser.print_usage())

    sub_parser = parser.add_subparsers()

    add_parser = sub_parser.add_parser(
        "add",
        help="add file to local repo"
    )
    add_parser.set_defaults(command=add_command)
    add_parser.add_argument(
        "file",
        help="File to start tracking"
    )

    info_parser = sub_parser.add_parser(
        "info",
        help="get info about the internal repo"
    )
    info_parser.set_defaults(command=info_command)

    return parser


def add_command(args: argparse.Namespace) -> None:
    """
    Add hardlink to file in repo with proper name scheme to be applied
    :param args:
    :return:
    """
    if not os.path.exists(args.file):
        print(f"Error {args.file} doesn't exist")

    print(os.path.abspath(args.file))

    pass


def info_command(args: argparse.Namespace) -> None:
    """
    List out information about the internal repo
    :param args:
    :return:
    """
    print("TODO: Info")
    pass
