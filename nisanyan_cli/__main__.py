import argparse
from .cli import Niscli

__version__ = "0.0.2"

# parse arguments
argparser = argparse.ArgumentParser(prog="nisanyan_cli")
argparser.add_argument(
    "word",
    type=str,
    nargs="*",
    help="<word>",
)
argparser.add_argument(
    "-p", "--plain", action="store_true", help="returns plain output"
)
argparser.add_argument(
    "-v", "--version", action="version", version="%(prog)s v" + __version__
)
args = argparser.parse_args()


def cli():
    word = " ".join(args.word)
    if len(args.word) > 0:
        if args.plain:
            Niscli(word).plain_output()
        else:
            Niscli(word).rich_output()
    else:
        print("kelime giriniz.")


if __name__ == "__main__":
    cli()
