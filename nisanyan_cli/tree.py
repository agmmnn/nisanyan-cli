from rich import print
from rich.tree import Tree
from urllib.parse import quote
from .langs_list import lang_dict
from .request import req


class Nistree:
    def __init__(self, word):
        self.word = quote(word)
        self.print_tree()

    def get_data(self):
        data = req(self.word)
        return data["words"]

    def print_tree(self):
        data = self.get_data()
        for j in data:
            tree = Tree(f"{self.word} [cyan](Günümüz Türkçesi)[/]")
            for i in j["etymologies"]:
                tree.add(
                    f'{i["romanizedText"]}({i["originalText"]}) ({i["languages"][0]["name"]}): [grey50]{i["definition"]}.[/]'
                )
            print(tree)
            print()
