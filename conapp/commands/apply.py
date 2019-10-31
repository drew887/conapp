import os
import argparse
import sys

from conapp.url_generators import RESOLVERS
from conapp.file_paths import get_repo_dir
from conapp.definitions import Hosts
from conapp.file_paths import check_dirs, create_dirs, get_config_dir, CONFIG_DIR_REPO
from conapp.file_ops import apply_snapshot, create_snapshot, download_file


#TODO: Rename this from apply to like config and have apply be a subcommand
COMMAND = 'apply'


def setup_arguments(sub_parser) -> argparse.ArgumentParser:
    """
    Setup the arguments for the apply command
    """
    parser = sub_parser.add_parser(COMMAND, help="apply a config")

    parser.set_defaults(command=main)
    parser.add_argument(
        '-u',
        '--user',
        required=True,
        help='username to pull from'
    )
    parser.add_argument(
        '-r',
        '--repo',
        default='config',
        help='repo name to pull, defaults to config'
    )
    parser.add_argument(
        '--no-download',
        action='store_true',
        help='Use already downloaded copy'
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
        '--no-apply',
        action="store_true",
        dest="no_apply",
        help="Don't actually run"
    )

    subparsers = parser.add_subparsers(
        title=f"{COMMAND} commands",
        description="sub commands for managing configs"
    )

    list_parser = subparsers.add_parser('list', help="list downloaded configs")

    list_parser.set_defaults(command=list_configs)

    return parser


def main(args: argparse.Namespace) -> None:
    """Download and Apply a snapshot"""
    repo_dir = get_repo_dir(args.user, args.repo)

    if not check_dirs([repo_dir]):
        create_dirs([repo_dir])

    file_name = repo_dir + "/" + f"{args.user}.{args.repo}.tar.gz"

    if args.no_download and os.path.isfile(file_name):
        print(f"no-download passed, applying local file {file_name}")
    else:
        if args.no_download:
            print("Error: no-download passed but no local copy to apply!")
            sys.exit(2)
        else:
            download_file(
                file_name,
                RESOLVERS.get(args.host)(args.user, args.repo)
            )

    if args.no_apply:
        print(f"--no-apply passed, not applying {file_name}")
    else:
        create_snapshot(file_name)

        if input("About to override files, really apply? [y/N]: ") == 'y':
            apply_snapshot(file_name)
        else:
            print(f"Not applying {file_name}")


def list_configs(args: argparse.Namespace) -> None:
    repo_dir = get_config_dir(CONFIG_DIR_REPO)
    users = {}

   #NOTE: This could probably be done with os.walk and save some fs calls
   #  however there would be a bunch of additional checking needed to be done since its a flat list instead of nested w
    for user_dir in os.scandir(repo_dir):
        if user_dir.is_dir():
            repos = []

            for user_repo_dir in os.scandir(user_dir.path):
                if user_repo_dir.is_dir and len(os.listdir(user_repo_dir.path)) > 0:
                    repos.append(user_repo_dir.name)

            if len(repos) > 0:
                users[user_dir.name]=repos

    if args.user is not None:
        if args.user in users:
            print_user(args.user, users[args.user])
        else:
            print(f"user {args.user} has no downloaded configs")
    else:
        print("Downloaded configs are: ")
        for user, repos in users:
            print_user(user, repos)
            print("---")

def print_user(user: str, repos: list) -> None:
    print(f"{user}:")
    for repo in repos:
        print(f" {repo}")
