from enum import Enum

COMMANDS = {
    'apply': 1,
    # 'track': 2,
    # 'commit': 3,
}

class Hosts(Enum):
    BITBUCKET = 'B'
    GITHUB = 'G'

