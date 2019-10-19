#!/usr/bin/env python3

import argparse
import urllib.request
from swat.arguments import validate_args, get_args
from swat.url_generators import RESOLVERS
from swat.file_paths import *
from swat.tar import get_tar_cmd
import subprocess
import os


def apply_snapshot(file_name: str) -> None:
    print(get_tar_cmd(flags=[
        'z',
        'v',
        'x',
        ('f', file_name),
        ('C', '~/')
    ]))


def create_snapshot(file_name):
    get_file_names_command = [
        "tar",
        '--strip-components=1',
        '--show-transformed-names',
        '-tf',
        file_name
    ]
    tar_command_result = subprocess.run(
        get_file_names_command,
        text=True,
        capture_output=True
    )

    if tar_command_result.returncode is not 0:
        print(f"Error while running tar command!!!\n"
              f"| Command was: {' '.join(get_file_names_command)}\n"
              f"| Error was: {tar_command_result.stderr}\n"
              f"| return code is: {tar_command_result.returncode}")
        exit(tar_command_result.returncode)

    files = tar_command_result.stdout.split()
    files = list(map(lambda x: f"{x}", filter(lambda x: x is not "/", files)))

    print(' '.join([
        'tar',
        '-C',
        os.path.expanduser('~'),
        '-czvf',
        get_snapshot_filename(),
        ' '.join(files)
    ]))


def main(args: argparse.Namespace) -> None:
    if not validate_args(args):
        exit(-1)

    if not check_dirs(args.user, args.repo):
        print("creating config dirs...")
        create_dirs(args.user, args.repo)

    url = RESOLVERS.get(args.host)(args.user, args.repo)
    file_name = get_repo_dir(args.user, args.repo) + "/" + f"{args.user}.{args.repo}.tar.gz"

    # download_file(file_name, url)
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
