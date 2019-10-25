from conapp.arguments import get_args
from conapp.file_paths import check_dirs, create_dirs


def main() -> None:
    args = get_args()

    if not check_dirs(args.user, args.repo):
        print("creating config dirs...")
        create_dirs(args.user, args.repo)


if __name__ == "__main__":
    main()
