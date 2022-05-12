from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.align import Align
from urllib.parse import quote
from .request import req
from ._utils import *


class Niscli:
    def __init__(self, word, request):
        self.word = quote(word)
        self.request = request
        self.print_data()

    def get_data(self):
        output = {}
        data = self.request
        for i in data["words"]:

            try:
                maddeye_gonderenler = [j["name"] for j in i["referenceOf"]]
            except:
                maddeye_gonderenler = []

            try:
                daha_fazla = [j["name"] for j in i["references"]]
            except:
                daha_fazla = []

            try:
                lst = []
                tarihce = ""
                for j in i["histories"]:
                    txt = (
                        (f'{j["language"]["name"]}: ' if "language" in j else "")
                        + (f'"{j["definition"]}" ' if j["definition"] != "" else "")
                        + (f'{j["excerpt"]} ' if j["excerpt"] != "" else "")
                        + f'[grey50][{(j["source"]["name"]+", ") if j["source"]["name"]!=""else ""}{j["source"]["book"]}, {j["date"]}][/]'
                    )
                    quote = replace_chars(
                        j["quote"].replace("[", "〔").replace("]", "〕")
                    )
                    lst.append([txt, quote])
                for j in lst:
                    tarihce = (
                        tarihce
                        + f"{j[0]}\n  [i aquamarine1]{j[1]}[/]"
                        + ("\n" if j != lst[-1] else "")
                    )
            except:
                tarihce = None
            try:
                lst = []
                koken = ""
                for j in i["etymologies"]:
                    txt = (
                        f'{j["languages"][0]["name"]} {j["romanizedText"]} {(j["originalText"]+" " if j["originalText"]!=""else"")}'
                        + ('"' + j["definition"] + '"' if j["definition"] != "" else "")
                    )
                    lst.append(txt)
                for j in lst:
                    koken = koken + j + ". "
            except:
                koken = None

            output[i["name"]] = {
                "koken": koken,
                "daha_fazla": daha_fazla,
                "ek_aciklama": replace_chars(i["note"]) if i["note"] else None,
                "benzer_sozcukler": i["queries"],
                "maddeye_gonderenler": maddeye_gonderenler,
                "tarihce": tarihce,
                "son_guncelleme": date_convert(i["timeUpdated"][:10]),
            }
        return output

    def print_data(self):
        data = self.get_data()
        # print(data)
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
            table.add_row(
                "[#994E8E]Köken:[/#994E8E]\n" + data[i]["koken"] + "\n"
            ) if data[i]["koken"] else None
            table.add_row(
                "Daha fazla bilgi için [cornflower_blue]"
                + "[/], [cornflower_blue]".join(data[i]["daha_fazla"])
                + "[/] "
                + ("maddesine" if len(data[i]["daha_fazla"]) == 1 else "maddelerine")
                + " bakınız."
                + "\n"
            ) if data[i]["daha_fazla"] else None
            table.add_row(
                "[#994E8E]Ek açıklama:[/#994E8E]\n" + data[i]["ek_aciklama"] + "\n"
            ) if data[i]["ek_aciklama"] else None
            table.add_row(
                "[#994E8E]Benzer sözcükler:[/#994E8E]\n"
                + ", ".join(data[i]["benzer_sozcukler"][:20])
                + "\n"
            ) if data[i]["benzer_sozcukler"] else None
            table.add_row(
                "[#994E8E]Bu maddeye gönderenler:[/#994E8E]\n[cornflower_blue]"
                + "[/], [cornflower_blue]".join(data[i]["maddeye_gonderenler"][:24])
                + "[/]\n"
            ) if data[i]["maddeye_gonderenler"] else None
            table.add_row(
                "[#994E8E]Tarihçe: (tespit edilen en eski Türkçe kaynak ve diğer örnekler)[/#994E8E]\n"
                + data[i]["tarihce"]
            ) if data[i]["tarihce"] else None
            print(table)
        Console().print(
            f"[grey42][link=https://www.nisanyansozluk.com/kelime/{self.word}]nisanyansozluk.com↗[/link]",
            justify="right",
        )
