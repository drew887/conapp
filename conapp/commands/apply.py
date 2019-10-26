import subprocess
import os
import argparse
import urllib.request
import sys

from conapp.url_generators import RESOLVERS
from conapp.file_paths import get_repo_dir, get_snapshot_filename
from conapp.validate import validate_subprocess
from conapp.definitions import USER_HOME_DIR, DEFAULT_STRIP_COMPONENTS, Hosts


COMMAND = 'apply'


def validate(args: argparse.Namespace) -> bool:
    # Nothing extra to do yet
    return True


def setup_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Setup the arguments for the apply command
    """

    parser.set_defaults(command=COMMAND)
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
        '--dry-run',
        action="store_true",
        dest="dry_run",
        help="Don't actually run"
    )

    return parser


def main(args: argparse.Namespace) -> None:
    """Download and Apply a snapshot"""

    file_name = get_repo_dir(args.user, args.repo) + \
        "/" + f"{args.user}.{args.repo}.tar.gz"

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

    if args.dry_run:
        print(f"dry run, applying {file_name}")
    else:
        create_snapshot(file_name)
        apply_snapshot(file_name)


def apply_snapshot(file_name: str) -> None:
    """Given file_name use tar to apply it to the users home directory"""

    print(f"Applying snapshot {file_name}")

    validate_subprocess(
        subprocess.run([
            'tar',
            '-C',
            USER_HOME_DIR,
            DEFAULT_STRIP_COMPONENTS,
            '--show-transformed-names',
            '-zvxf',
            file_name,
        ])
    )


def create_snapshot(file_name):
    get_file_names_command = [
        "tar",
        DEFAULT_STRIP_COMPONENTS,
        '--show-transformed-names',
        '-tf',
        file_name
    ]
    get_file_names_command_result = subprocess.run(
        get_file_names_command,
        text=True,
        capture_output=True
    )

    validate_subprocess(get_file_names_command_result)

    files = list(
        filter(
            lambda file_path: os.path.isfile(
                os.path.expanduser(f"~/{file_path}")),
            get_file_names_command_result.stdout.split()
        )
    )

    if len(files) > 0:
        snapshot_name = get_snapshot_filename()
        backup_command = [
            'tar',
            '-C',
            USER_HOME_DIR,
            '-czvf',
            snapshot_name,
        ] + files

        print(
            f"Local files would get overridden, creating backup of: {' '.join(files)}")

        validate_subprocess(subprocess.run(
            backup_command,
            text=True,
            capture_output=True
        ))

        print(f"Successfully backed up files to {snapshot_name}")

    else:
        print("No files will be overridden, not creating backup")


def download_file(file_name: str, url: str) -> None:
    """Attempt to download a file or exit"""

    try:
        print(f"Attempting to download {url}")
        urllib.request.urlretrieve(url, file_name)
        print(f"Success, downloaded to {file_name}")
    except urllib.request.HTTPError as ex:
        print(f"Error occurred, does {url} exist?\n{ex}")
        sys.exit(-1)
