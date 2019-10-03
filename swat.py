#!/usr/bin/env python3

import argparse
import os
import sys

from typing import List, Tuple, Union

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


def get_tar_cmd(*args, flags: List[Union[Tuple[str, str], str]]) -> str:
    result = "tar "

    for flag in flags:
        if type(flag) is str:
            result = result + f"-{flag} "
        else:
            result = result + f"-{flag[0]} {flag[1]} "

    return result + ' '.join(args)


def main():
    print(get_tar_cmd("sdfs", flags=TAR_CREATE_FLAGS))


if __name__ == '__main__':
    main()
