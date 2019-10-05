#!/usr/bin/env python3

import argparse
import os
import sys
import url_generators

from typing import List, Tuple, Union
from enum import Enum

# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
#
# args = parser.parse_args()
# print(args.accumulate(args.integers))1

TAR_CREATE_FLAGS = [
    'c', 'v', 'z'
]


class Hosts(Enum):
    BITBUCKET = 'B'
    GITHUB = 'G'


def get_tar_cmd(*args, flags: List[Union[Tuple[str, str], str]]) -> str:
    """
    Python has support for tarfile, but it doesn't have built in support for
    tar's `--strip 1` so its easier to just crap out tar commands
    """
    result = "tar "

    for flag in flags:
        if type(flag) is str:
            result = result + f"-{flag} "
        else:
            result = result + f"-{flag[0]} {flag[1]} "

    return result + ' '.join(args)


def main(args: argparse.Namespace) -> None:
    print(args)
    test = url_generators.get_bitbucket_url

    if (args.host == Hosts.GITHUB):
        test = url_generators.get_github_url


    print(test(args.user))


def getArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='a Shitty Wrapper Around Tar')

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

    return parser.parse_args()


if __name__ == '__main__':
    main(getArgs())
