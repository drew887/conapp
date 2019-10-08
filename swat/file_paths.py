import os

CONFIG_DIR = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser("~/")) + ".config/swat"

CONFIG_DIRS = [
    "snapshots",
    "repo"
]


def get_config_dir(dir: str) -> str:
    return CONFIG_DIR + '/' + dir


def check_dirs() -> bool:
    result = False

    for conf_dir in CONFIG_DIRS:
        result = result or os.path.isdir(get_config_dir(conf_dir))

    return result


def create_dirs() -> None:
    for config_dir in CONFIG_DIRS:
        os.makedirs(get_config_dir(config_dir))
