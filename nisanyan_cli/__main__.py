import argparse
from .cli import Niscli

__version__ = "0.1"

# parse arguments
argparser = argparse.ArgumentParser(prog="nisanyan_cli")
argparser.add_argument(
    "word",
    type=str,
    nargs="*",
    help="<word>",
)
argparser.add_argument(
    "-v", "--version", action="version", version="%(prog)s v" + __version__
)
args = argparser.parse_args()


def cli():
    word = " ".join(args.word)
    Niscli(word)


if __name__ == "__main__":
    cli()
