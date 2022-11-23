from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import print
from ._adlar_cache import cache
from urllib.parse import quote
from http.client import HTTPSConnection
from json import loads


def req(name):
    conn = HTTPSConnection("radyal-api.vercel.app")
    conn.request("GET", f"/api/nisanyanadlar-decrypt?name={name}")
    res = conn.getresponse()
    data = res.read()
    return loads(data)


class Nisadlar:
    def __init__(self, name):
        self.name = name
        self.data = req(quote(name))
        self.print_rich()

    def print_rich(self):
        sex_symbol = {"K": "\u2640", "E": "\u2642"}
        for i in self.data["names"]:
            table = Table(box=box.ROUNDED, show_footer=True, expand=True)
            table.add_column(
                f'{sex_symbol[i["sex"]]} {i["entry"]} [grey42]({i["cumulative"]} kişi)[/]',
                header_style="bold",
                footer=Align(
                    f'sıklık sırası: {i["frequency"]}',
                    vertical="middle",
                    align="center",
                    style="grey42",
                ),
            )
            # cache["nations"] nat_code=yt : cache["languages"] lang_code:t
            table.add_row("[#994E8E]Köken:[/#994E8E]" + "\n" + i["means"] + "\n") if i[
                "means"
            ] else None
            table.add_row((i["note"]) + "\n") if i["note"] else None
            # 0: ulusal t: türkçe alanı
            table.add_row(
                "[#994E8E]Dağılım:[/#994E8E]" + "\n" + i["region"] + "\n"
            ) if i["region"] else None
            table.add_row(
                "[#994E8E]Farklı Yazılışlar:[/#994E8E]"
                + "\n"
                + ", ".join([f'{j["name"]} ({j["count"]})' for j in i["variants"]])
                + "\n"
            ) if i["variants"] else None
            table.add_row(
                "[#994E8E]İlgili Adlar:[/#994E8E]" + "\n" + ", ".join(i["relatedNames"])
            ) if i["region"] else None

            print(table)
        Console().print(
            f"[grey42][link=https://www.nisanyanadlar.com/isim/{quote(self.name)}]nisanyansozluk.com↗[/link]",
            justify="right",
        )
