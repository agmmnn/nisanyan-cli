from argparse import ArgumentParser
from importlib_metadata import version
from urllib.parse import quote
from rich import print

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
    clr = 238
    fiveBefore, fiveAfter = [], []
    for b, a in zip(request.get("fiveBefore", [])[::-1], request.get("fiveAfter", [])):
        clr = clr - 25
        fiveBefore.append(f"[rgb({clr},{clr},{clr})]" + b["name"] + "[/]")
        fiveAfter.append(f"[rgb({clr},{clr},{clr})]" + a["name"] + "[/]")
    print("[i cyan]Kelime bulunamadı. Yakın sonuçlar:[/]")

    # Check if request['words'] exists and has elements to avoid IndexError
    current_word = request.get("words", [{}])[0].get("name", "")

    print(
        f'{", ".join(fiveBefore[::-1])}, {current_word}, {", ".join(fiveAfter)}'
    )
    print()


def cli():
    if args.ad:
        name = " ".join(args.word)
        Nisadlar(name, args.random).run()
    elif args.word:
        word = " ".join(args.word)
        request = req(f"/api/words/{quote(word)}")
        if request.get("isUnsuccessful"):
            close_words(word, request)
            exit()
        if not args.tree:
            Niscli(word, request, args.plain).display()
        else:
            Nistree(word, request).display()
    elif args.random:
        # Check if random word fetch is successful
        rand_res = req("/api/words/nonexistword")
        if not rand_res or "randomWord" not in rand_res:
             print("[red]Error fetching random word.[/]")
             exit(1)

        word = rand_res["randomWord"]["name"]
        request = req(f"/api/words/{quote(word)}")
        if not args.tree:
            Niscli(word, request, args.plain).display()
        else:
            Nistree(word, request).display()
    else:
        argparser.print_help()


if __name__ == "__main__":
    cli()
