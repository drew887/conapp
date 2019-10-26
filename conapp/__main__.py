import sys

from conapp.arguments import get_args, validate_args, COMMANDS
from conapp.file_paths import check_dirs, create_dirs


def main() -> None:
    args = get_args(sys.argv)

    if not validate_args(args):
        sys.exit(1)

    if not check_dirs(args.user, args.repo):
        print("creating config dirs...")
        create_dirs(args.user, args.repo)

    command = COMMANDS.get(
        args.command,
        None
    )

    if command is None:
        print("Error, Command not found?")
        sys.exit(-1)
    else:
        command(args)


if __name__ == "__main__":
    main()
