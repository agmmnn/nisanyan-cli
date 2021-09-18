from nisanyan_cli.cli import main
import argparse

# parse arguments
argparser = argparse.ArgumentParser(prog="nisanyan_cli")
argparser.add_argument(
    "words",
    type=str,
    nargs="*",
    help="[first word] [last word]",
)
# argparser.add_argument("-l", "--list", action="store_true", default=True)
args = argparser.parse_args()


def cli():
    if len(args.words) > 0:
        main("".join(args.words))
    else:
        print("kelime giriniz.")


if __name__ == "__main__":
    cli()
