from typing import List, Tuple, Union

TAR_CREATE_FLAGS = [
    'c', 'v', 'z'
]


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

    return (result + ' '.join(args)).strip()
