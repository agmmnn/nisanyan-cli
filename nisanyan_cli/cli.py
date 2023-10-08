from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.align import Align
from urllib.parse import quote
from .request import req
from ._utils import *

TITLES = {
    "koken": "Köken:",
    "daha_fazla": "Daha fazla bilgi için",
    "ek_aciklama": "Ek Açıklama:",
    "benzer_sozcukler": "Benzer Sözcükler:",
    "maddeye_gonderenler": "Bu maddeye gönderenler:",
    "tarihce": "Tarihçe: (tespit edilen en eski Türkçe kaynak ve diğer örnekler)",
    "son_guncelleme": "Son Güncelleme",
}


class Niscli:
    def __init__(self, word, request, plain):
        self.word = word
        self.request = request
        if plain:
            self.print_plain()
            exit()
        self.print_rich()

    def get_data(self):
        output = {}
        data = self.request
        for i in data["words"]:
            # Köken
            try:
                lst = []
                koken = ""
                for j in i["etymologies"]:
                    txt = (
                        f'[b]{j["languages"][0]["name"]}[/] [i]{j["romanizedText"]}[/] {(j["originalText"]+" " if j["originalText"]!=""else"")}'
                        + ("“" + j["definition"] + "”" if j["definition"] != "" else "")
                    )
                    lst.append(txt)
                for j in lst:
                    koken = koken + j + ". "
            except:
                koken = None
            # Daha fazla
            try:
                daha_fazla = [j["name"] for j in i["references"]]
            except:
                daha_fazla = []
            # Bu maddeye gönderenler
            try:
                maddeye_gonderenler = [j["name"] for j in i["referenceOf"]]
            except:
                maddeye_gonderenler = []
            # Tarihçe
            try:
                lst = []
                tarihce = ""
                for j in i["histories"]:
                    txt = (
                        (f'{j["language"]["name"]}: ' if "language" in j else "")
                        + (f'"{j["definition"]}" ' if j["definition"] != "" else "")
                        + (f'[i]{j["excerpt"]}[/] ' if j["excerpt"] != "" else "")
                        + f'[grey50][{(j["source"]["name"]+", ") if j["source"]["name"]!=""else ""}{j["source"]["book"]}, {j["date"]}][/]'
                    )
                    quote = replace_chars(
                        j["quote"].replace("[", "〔").replace("]", "〕")
                    )
                    lst.append([txt, quote])
                for j in lst:
                    tarihce = (
                        tarihce
                        + j[0]
                        + (f"\n  [i]{j[1]}[/]" if j[1] != "" else "")
                        + ("\n" if j != lst[-1] else "")
                    )
            except:
                tarihce = None

            output[i["name"]] = {
                "koken": replace_chars(koken) if koken else None,
                "daha_fazla": daha_fazla,
                "ek_aciklama": replace_chars(i["note"]) if i["note"] else None,
                "benzer_sozcukler": [j for j in i["queries"] if j != i["name"]],
                "maddeye_gonderenler": maddeye_gonderenler,
                "tarihce": tarihce,
                "son_guncelleme": date_convert(i["timeUpdated"][:10]),
            }
        return output

    def print_rich(self):
        data = self.get_data()
        data2 = {}
        for i in data:
            data2[i] = {}
            for j in data[i]:
                if data[i][j]:
                    data2[i][j] = data[i][j]
        data = data2

        for i in data:
            table = Table(box=box.ROUNDED, show_footer=True, expand=True)
            table.add_column(
                i,
                header_style="bold",
                footer=Align(
                    data[i]["son_guncelleme"],
                    vertical="middle",
                    align="right",
                    style="grey42",
                ),
            )
            for jx, j in enumerate(data[i]):
                newline = "" if jx == len(list(data[i].keys())) - 2 else "\n"
                if j == "son_guncelleme":
                    continue
                if j == "daha_fazla" and data[i][j]:
                    table.add_row(
                        f"{TITLES[j]} [cornflower_blue]"
                        + "[/], [cornflower_blue]".join(data[i][j])
                        + "[/] "
                        + ("maddesine" if len(data[i][j]) == 1 else "maddelerine")
                        + " bakınız."
                        + newline
                    )
                    continue
                if data[i][j]:
                    content = data[i][j]
                    title = f"[#994E8E]{TITLES[j]}[/#994E8E]\n"
                    table.add_row(
                        title
                        + (
                            content
                            if type(content) != list
                            else ", ".join(content[:20])
                        )
                        + newline
                    )
            print(table)

        Console().print(
            f"[grey42][link=https://www.nisanyansozluk.com/kelime/{quote(self.word)}]nisanyansozluk.com/kelime/{self.word}↗[/link]",
            justify="right",
        )

    def print_plain(self):
        data = self.get_data()
        console = Console(no_color=True)
        for i in data:
            console.print(f":::...{i}...:::")
            for j in data[i]:
                elem = data[i][j]
                if j == "son_guncelleme":
                    continue
                if j == "daha_fazla" and elem:
                    console.print(
                        f"{TITLES[j]} "
                        + ", ".join(elem)
                        + (" maddesine" if len(elem) == 1 else " maddelerine")
                        + " bakınız.\n"
                    )
                    continue
                if elem:
                    elem = elem if type(elem) != list else ", ".join(elem)
                    console.print(f"{TITLES[j]}\n{elem}\n") if elem else None
