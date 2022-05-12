from argparse import ArgumentParser
from urllib.parse import quote
from .tree import Nistree
from .cli import Niscli
from .request import req

__version__ = "0.3.0"

# parse arguments
argparser = ArgumentParser(prog="nisanyan_cli")
argparser.add_argument(
    "word",
    type=str,
    nargs="*",
    help="<word>",
)
argparser.add_argument(
    "-t",
    "--tree",
    action="store_true",
    default=False,
    help="show result as etymology tree",
)
argparser.add_argument(
    "-r",
    "--random",
    action="store_true",
    default=False,
    help="selects a random word and brings the result",
)
argparser.add_argument(
    "-v", "--version", action="version", version="%(prog)s v" + __version__
)
args = argparser.parse_args()


def close_words(word, request):
    from rich import print

    clr = 238
    fiveBefore, fiveAfter = [], []
    for (b, a) in zip(request["fiveBefore"][::-1], request["fiveAfter"]):
        clr = clr - 25
        fiveBefore.append(f"[rgb({clr},{clr},{clr})]" + b["name"] + "[/]")
        fiveAfter.append(f"[rgb({clr},{clr},{clr})]" + a["name"] + "[/]")
    print("[i cyan]Girdiğiniz kelime bulunamadı. Yakın sonuçlar:[/]")
    print(
        f'{", ".join(fiveBefore[::-1])}, {request["words"][0]["name"]}, {", ".join(fiveAfter)}'
    )
    print()


def cli():
    if args.word:
        word = " ".join(args.word)
        request = req(quote(word))
        if request["isUnsuccessful"]:
            close_words(word, request)
            exit()
        if not args.tree:
            Niscli(word, request)
        else:
            Nistree(word, request)
    elif args.random:
        request = req("ab")
        word = request["randomWord"]["name"]
        if not args.tree:
            Niscli(word, request)
        else:
            Nistree(word, request)
    else:
        print("Kelime girmediniz.")


if __name__ == "__main__":
    cli()
