import os
import argparse

from conapp.file_paths import CONFIG_TRACK_DIR

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
    add_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite if already tracked"
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
    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        print(f"Error {args.file} doesn't exist or isn't a file")
        print("conapp currently doesn't track folders")

    abs_path = os.path.abspath(args.file)
    home_path = os.path.expanduser("~")

    if abs_path.startswith(home_path):
        # we gotta chop off the leading '/' as well
        relative_home_path = abs_path[(len(home_path) + 1):]
        abs_track_path = os.path.join(CONFIG_TRACK_DIR, relative_home_path)

        if args.force or not os.path.exists(abs_track_path):
            if input(f"track {abs_track_path} ? [y/N]: ") == 'y':
                # create any leading folders needed
                # TODO: add flag to disable this and just add at top level
                leading_track_folder = abs_track_path[0:abs_track_path.rfind("/")]

                if not os.path.exists(leading_track_folder):
                    os.makedirs(leading_track_folder)

                # TODO: Add extra flags to control how file makes it into repo

                if args.force and os.path.exists(abs_track_path):
                    print("Removing old file")
                    os.remove(abs_track_path)

                print("Tracking file via hardlink")
                os.link(abs_path, abs_track_path)
            else:
                print("Not tracking file")
        else:
            print("File already tracked")

    pass


def info_command(args: argparse.Namespace) -> None:
    """
    List out information about the internal repo
    :param args:
    :return:
    """
    print("TODO: Info")
    pass
