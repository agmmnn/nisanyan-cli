import argparse
from .cli import Niscli
from .tree import Nistree

__version__ = "0.2.1"

# parse arguments
argparser = argparse.ArgumentParser(prog="nisanyan_cli")
argparser.add_argument(
    "word",
    type=str,
    nargs="*",
    help="<word>",
)
argparser.add_argument(
    "--tree",
    "-t",
    action="store_true",
    default=False,
    help="show result as etymology tree",
)
argparser.add_argument(
    "-v", "--version", action="version", version="%(prog)s v" + __version__
)
args = argparser.parse_args()


def cli():
    word = " ".join(args.word)
    if args.tree:
        Nistree(word)
    else:
        Niscli(word)


if __name__ == "__main__":
    cli()
