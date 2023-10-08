from rich import print
from rich.tree import Tree
from urllib.parse import quote
from ._langlist import lang_dict
from ._utils import replace_chars


class Nistree:
    def __init__(self, word, request):
        self.word = quote(word)
        self.request = request
        self.print_tree()

    def print_tree(self):
        sublist = ["bileşik sözcük", "bileşik sözcüğün devamı", "veya"]
        word = self.request["words"]
        for idx, word in enumerate(word):
            tree = Tree(
                f'{self.request["words"][idx]["name"]} [cyan](Günümüz Türkçesi)[/]'
            )
            lst = []
            try:
                for i in word["etymologies"]:
                    lang = i["languages"][0]["name"]
                    dil = (
                        f"({lang})"
                        if lang not in lang_dict
                        else (
                            f'[cyan]([link={lang_dict[lang]["wiki_link"]}]'
                            + lang_dict[lang]["name"]
                            + "[/link]"
                            + f' {lang_dict[lang]["era"]})'
                        )
                    )
                    lst.append(
                        (
                            (
                                f'[i cyan][link=https://www.nisanyansozluk.com/ek/{quote(i["affixes"]["prefix"]["name"])}]'
                                + i["affixes"]["prefix"]["name"]
                                + "[/][/] "
                            )
                            if (i["affixes"] != {} and "prefix" in i["affixes"])
                            else ""
                        )
                        + i["romanizedText"]
                        + (
                            (" ‹" + i["originalText"] + "›")
                            if i["originalText"] != ""
                            else ""
                        )
                        + (
                            (
                                f' [i cyan][link=https://www.nisanyansozluk.com/ek/{quote(i["affixes"]["suffix"]["name"])}]'
                                + i["affixes"]["suffix"]["name"]
                                + "[/][/]"
                            )
                            if (i["affixes"] != {} and "suffix" in i["affixes"])
                            else ""
                        )
                        + f" [cyan]{dil}[/]"
                        + (
                            (": [grey50]" + replace_chars(i["definition"]) + ".[/]")
                            if i["definition"] != ""
                            else ""
                        )
                    )
            except:
                continue

            sub = {}
            sub[lst[0]] = tree.add(lst[0])
            last1 = sub[lst[0]]
            if len(lst) > 1:
                for ix, i in enumerate(lst[1:]):
                    if word["etymologies"][ix + 1]["relation"]["name"] not in sublist:
                        sub[i] = sub[list(sub.keys())[-1]].add(i)
                        last1 = sub[list(sub.keys())[-1]]
                    else:
                        sub[i] = last1.add(i)
            print(tree)
            print()
