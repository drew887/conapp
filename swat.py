#!/usr/bin/env python3

import argparse
from swat.arguments import validate_args, get_args
from swat.url_generators import RESOLVERS


def main(args: argparse.Namespace) -> None:
    if not validate_args(args):
        exit(-1)

    print(RESOLVERS.get(args.host)(args.user, args.repo))


if __name__ == '__main__':
    main(get_args())
