import os

from datetime import datetime

CONFIG_DIR = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser("~/")) + ".config/conapp"
CONFIG_DIR_REPO = "repo"
CONFIG_DIR_SNAPSHOT = "snapshots"


def get_config_dir(dir: str) -> str:
    """Get a directory prefixed in the config dir"""
    return CONFIG_DIR + '/' + dir


CONFIG_DIRS = [
    get_config_dir(CONFIG_DIR_SNAPSHOT),
    get_config_dir(CONFIG_DIR_REPO)
]


# TODO: Abstract repo default into a constant somewhere
def get_repo_dir(user: str, repo: str) -> str:
    return get_config_dir(CONFIG_DIR_REPO) + "/" + user + "/" + repo


def get_snapshot_filename() -> str:
    return get_config_dir(CONFIG_DIR_SNAPSHOT) \
           + "/" \
           + datetime.now().strftime("%Y-%m-%d.%H-%M-%S") \
           + ".tar.gz"


def check_dirs(user: str, repo: str) -> bool:
    user_dir = get_repo_dir(user, repo)

    for config_dir in CONFIG_DIRS + [user_dir]:
        if not os.path.isdir(config_dir):
            return False

    return True


def create_dirs(user: str, repo: str) -> None:
    """
    Create the directories required to operate
    """
    user_dir = get_repo_dir(user, repo)

    for config_dir in CONFIG_DIRS + [user_dir]:
        try:
            os.makedirs(config_dir)
        except FileExistsError:
            print(f"{config_dir} already exists, not recreating")
            continue
