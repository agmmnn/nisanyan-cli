from argparse import ArgumentParser
from importlib_metadata import version
from urllib.parse import quote

from .tree import Nistree
from .cli import Niscli
from .adlar import Nisadlar
from .request import req


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
    "-p",
    "--plain",
    action="store_true",
    default=False,
    help="plain text output",
)
argparser.add_argument(
    "-ad",
    action="store_true",
    default=False,
    help="show result from nisanyanadlar",
)
argparser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"nisanyan-cli {version('nisanyan-cli')}",
)
args = argparser.parse_args()


def close_words(word, request):
    from rich import print

    clr = 238
    fiveBefore, fiveAfter = [], []
    for b, a in zip(request["fiveBefore"][::-1], request["fiveAfter"]):
        clr = clr - 25
        fiveBefore.append(f"[rgb({clr},{clr},{clr})]" + b["name"] + "[/]")
        fiveAfter.append(f"[rgb({clr},{clr},{clr})]" + a["name"] + "[/]")
    print("[i cyan]Kelime bulunamadı. Yakın sonuçlar:[/]")
    print(
        f'{", ".join(fiveBefore[::-1])}, {request["words"][0]["name"]}, {", ".join(fiveAfter)}'
    )
    print()


def cli():
    if args.ad:
        name = " ".join(args.word)
        Nisadlar(name, args.random)
    elif args.word:
        word = " ".join(args.word)
        request = req(quote(word))
        if request["isUnsuccessful"]:
            close_words(word, request)
            exit()
        if not args.tree:
            Niscli(word, request, args.plain)
        else:
            Nistree(word, request)
    elif args.random:
        word = req("nonexistword")["randomWord"]["name"]
        request = req(quote(word))
        if not args.tree:
            Niscli(word, request, args.plain)
        else:
            Nistree(word, request)


if __name__ == "__main__":
    cli()
