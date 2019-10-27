import argparse

COMMAND = 'snapshots'


def setup_arguments(sub_parser) -> argparse.ArgumentParser:
    parser = sub_parser.add_parser(COMMAND, help="manage snapshots")

    parser.set_defaults(command=main)

    subparsers = parser.add_subparsers(
        title="snapshot commands",
        description="commands for managing snapshots"
    )

    list_parser = subparsers.add_parser('list', help="list snapshots")

    delete_parser = subparsers.add_parser('delete', help="remove snapshots")
    # TODO: Flush this out
    delete_parser.set_defaults(command=lambda x: print(f"deleting {x.file}"))
    delete_parser.add_argument(
        'file'
    )

    return parser


def main(x):
    print(x)
    pass
