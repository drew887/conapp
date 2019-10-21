#!/usr/bin/env python3

import argparse
import urllib.request
from conapp.arguments import validate_args, get_args
from conapp.url_generators import RESOLVERS
from conapp.file_paths import *
from conapp.validate import validate_subprocess
from conapp.definitions import DEFAULT_STRIP_COMPONENTS
import subprocess
import os

USER_HOME_DIR = os.path.expanduser('~')


def apply_snapshot(file_name: str) -> None:
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
            lambda file_path: os.path.isfile(os.path.expanduser(f"~/{file_path}")),
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

        print(f"Local files would get overridden, creating backup of: {' '.join(files)}")

        validate_subprocess(subprocess.run(
            backup_command,
            text=True,
            capture_output=True
        ))

        print(f"Successfully backed up files to {snapshot_name}")

    else:
        print("No files will be overridden, not creating backup")


def main(args: argparse.Namespace) -> None:
    if not validate_args(args):
        exit(-1)

    if not check_dirs(args.user, args.repo):
        print("creating config dirs...")
        create_dirs(args.user, args.repo)

    file_name = get_repo_dir(args.user, args.repo) + "/" + f"{args.user}.{args.repo}.tar.gz"

    if args.no_download and os.path.isfile(file_name):
        print(f"no-download passed, applying local file {file_name}")
    else:
        if args.no_download:
            print("Error: no-download passed but no local copy to apply!")
            exit(2)
        else:
            download_file(
                file_name,
                RESOLVERS.get(args.host)(args.user, args.repo)
            )

    create_snapshot(file_name)
    apply_snapshot(file_name)


def download_file(file_name: str, url: str) -> None:
    try:
        print(f"Attempting to download {url}")
        urllib.request.urlretrieve(url, file_name)
        print(f"Success, downloaded to {file_name}")
    except urllib.request.HTTPError as ex:
        print(f"Error occurred, does {url} exist?\n{ex}")
        exit(-1)


if __name__ == "__main__":
    main(get_args())
