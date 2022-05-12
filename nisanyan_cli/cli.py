from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.align import Align
from urllib.parse import quote
from .request import req


class Niscli:
    def __init__(self, word):
        self.word = quote(word)
        self.print_data()

    def get_data(self):
        output = {}
        data = req(self.word)
        for i in data["words"]:
            try:
                maddeye_gonderenler = [j["name"] for j in i["referenceOf"]]
            except:
                maddeye_gonderenler = []
            try:
                daha_fazla = [j["name"] for j in i["references"]]
            except:
                daha_fazla = []
            output[i["name"]] = {
                "koken": i["etymologies"],
                "daha_fazla": daha_fazla,
                "ek_aciklama": i["note"],
                "benzer_sozcukler": i["queries"],
                "maddeye_gonderenler": maddeye_gonderenler,
                "tarihce": i["histories"],
                "son_guncelleme": i["timeUpdated"],
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
                "[#994E8E]Köken:[/#994E8E]\n" + str(data[i]["koken"][0]) + "\n"
            )
            table.add_row(
                "Daha fazla bilgi için "
                + ", ".join(data[i]["daha_fazla"])
                + " maddesine bakınız."
                + "\n"
            ) if data[i]["daha_fazla"] else None
            table.add_row(
                "[#994E8E]Ek açıklama:[/#994E8E]\n" + data[i]["ek_aciklama"] + "\n"
            ) if data[i]["ek_aciklama"] else None
            table.add_row(
                "[#994E8E]Benzer sözcükler:[/#994E8E]\n"
                + ", ".join(data[i]["benzer_sozcukler"])
                + "\n"
            ) if data[i]["benzer_sozcukler"] else None
            table.add_row(
                "[#994E8E]Bu maddeye gönderenler:[/#994E8E]\n"
                + ", ".join(data[i]["maddeye_gonderenler"])
                + "\n"
            ) if data[i]["maddeye_gonderenler"] else None
            table.add_row(
                "[#994E8E]Tarihçe: (tespit edilen en eski Türkçe kaynak ve diğer örnekler)[/#994E8E]\n"
                + str(data[i]["tarihce"][0])
            ) if data[i]["tarihce"] else None
            print(table)
        Console().print(
            f"[grey42][link=https://www.nisanyansozluk.com/kelime/{self.word}]nisanyansozluk.com↗[/link]",
            justify="right",
        )
