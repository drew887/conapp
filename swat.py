#!/usr/bin/env python3

import argparse
import urllib.request
from swat.arguments import validate_args, get_args
from swat.url_generators import RESOLVERS
from swat.file_paths import *

def main(args: argparse.Namespace) -> None:
    if not validate_args(args):
        exit(-1)

    if not check_dirs():
        print("creating config dirs...")
        create_dirs()
    print(RESOLVERS.get(args.host)(args.user, args.repo))

    urllib.request.urlretrieve(RESOLVERS.get(args.host)(args.user, args.repo), f'{args.user}.{args.repo}.tar.gz')



if __name__ == '__main__':
    main(get_args())
