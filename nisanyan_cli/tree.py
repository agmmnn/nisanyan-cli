from rich import print
from rich.tree import Tree
from urllib.parse import quote
from ._langlist import lang_dict
from ._utils import replace_chars


class Nistree:
    def __init__(self, word, request):
        self.word = quote(word)
        self.request = request

    def display(self):
        self.print_tree()

    def print_tree(self):
        sublist = ["bileşik sözcük", "bileşik sözcüğün devamı", "veya"]
        words = self.request.get("words", [])

        for word_entry in words:
            tree = Tree(
                f'{word_entry["name"]} [cyan](Günümüz Türkçesi)[/]'
            )
            lst = []
            try:
                etymologies = word_entry.get("etymologies", [])
                for i in etymologies:
                    languages = i.get("languages", [])
                    if not languages:
                        continue

                    lang = languages[0]["name"]
                    if lang not in lang_dict:
                        dil = f"({lang})"
                    else:
                        lang_info = lang_dict[lang]
                        dil = (
                            f'[cyan]([link={lang_info["wiki_link"]}]'
                            + lang_info["name"]
                            + "[/link]"
                            + f' {lang_info["era"]})'
                        )

                    affixes = i.get("affixes", {})
                    prefix_str = ""
                    if affixes and "prefix" in affixes:
                         prefix_name = affixes["prefix"]["name"]
                         prefix_str = (
                            f'[i cyan][link=https://www.nisanyansozluk.com/ek/{quote(prefix_name)}]'
                            + prefix_name
                            + "[/][/] "
                         )

                    suffix_str = ""
                    if affixes and "suffix" in affixes:
                        suffix_name = affixes["suffix"]["name"]
                        suffix_str = (
                            f' [i cyan][link=https://www.nisanyansozluk.com/ek/{quote(suffix_name)}]'
                            + suffix_name
                            + "[/][/]"
                        )

                    definition_str = ""
                    definition = i.get("definition", "")
                    if definition:
                         definition_str = f": [grey50]{replace_chars(definition)}.[/]"

                    romanized = i.get("romanizedText", "")
                    original = i.get("originalText", "")
                    original_str = f" ‹{original}›" if original else ""

                    txt = (
                        prefix_str
                        + romanized
                        + original_str
                        + suffix_str
                        + f" [cyan]{dil}[/]"
                        + definition_str
                    )
                    lst.append(txt)

            except (KeyError, IndexError, TypeError):
                continue

            if not lst:
                continue

            sub = {}
            # Add the first element to the root tree
            sub[lst[0]] = tree.add(lst[0])
            last1 = sub[lst[0]]

            if len(lst) > 1:
                 for ix, item in enumerate(lst[1:]):
                     try:
                         relation = etymologies[ix+1]["relation"]["name"]
                     except (KeyError, IndexError):
                         relation = ""

                     if relation not in sublist:
                         # New branch from the previous node
                         parent_key = list(sub.keys())[-1]
                         parent_node = sub[parent_key]

                         sub[item] = parent_node.add(item)
                         # Drill down: subsequent items will be added to this new node
                         last1 = sub[item]
                     else:
                         # Add to the current context (last1)
                         sub[item] = last1.add(item)

            print(tree)
            print()
