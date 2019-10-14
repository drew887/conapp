#!/usr/bin/env python3

import argparse
import urllib.request
from swat.arguments import validate_args, get_args
from swat.url_generators import RESOLVERS
from swat.file_paths import *


def main(args: argparse.Namespace) -> None:
    if not validate_args(args):
        exit(-1)

    if not check_dirs(args.user, args.repo):
        print("creating config dirs...")
        create_dirs(args.user, args.repo)

    url = RESOLVERS.get(args.host)(args.user, args.repo)
    file_name = get_repo_dir(args.user, args.repo) + "/" + f"{args.user}.{args.repo}.tar.gz"

    download_file(file_name, url)


def download_file(file_name: str, url: str) -> None:
    try:
        print(f"Attempting to download {url}")
        urllib.request.urlretrieve(url, file_name)
        print(f"Success, downloaded to {file_name}")
    except urllib.request.HTTPError as ex:
        print(f"Error occurred, does {url} exist?\n{ex}")


if __name__ == "__main__":
    main(get_args())
