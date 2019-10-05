from enum import Enum

COMMANDS = {
    'apply': 1,
    'track': 2,
    'commit': 3,
}

TAR_CREATE_FLAGS = [
    'c', 'v', 'z'
]


class Hosts(Enum):
    BITBUCKET = 'B'
    GITHUB = 'G'

