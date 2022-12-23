from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import print
from ._adlar_cache import cache
from urllib.parse import quote
from http.client import HTTPSConnection
import json


def req(name):
    conn = HTTPSConnection("www.nisanyanadlar.com")
    conn.request(
        "GET", f"/_next/data/hFuzpyuQYJJeP-e3Q0pgO/isim/{name}.json?name={name}"
    )
    res = conn.getresponse()
    data = res.read()
    return json.loads(data)


class Nisadlar:
    def __init__(self, name, random: bool = False):

        if not name:
            self.name = "nonexistname"
        else:
            self.name = name.capitalize()

        self.data = req(quote(self.name))

        if random:
            self.name = self.data["pageProps"]["randomName"].capitalize()
            self.data = req(quote(self.name))
        elif self.name == "nonexistname":
            exit(1)
        elif self.data["pageProps"]["isUnsuccessful"]:
            print("Not found!")
            exit(1)

        self.rich_output()

    def rich_output(self):
        sex_symbol = {"K": "\u2640", "E": "\u2642"}
        for i in json.loads(self.data["pageProps"]["names"]):
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
            ) if i["variants"] else None
            table.add_row(
                "[#994E8E]İlgili Adlar:[/#994E8E]" + "\n" + ", ".join(i["relatedNames"])
            ) if i["relatedNames"] else None

            print(table)
        Console().print(
            f"[grey42][link=https://www.nisanyanadlar.com/isim/{quote(self.name)}]nisanyanadlar.com/isim/{self.name}↗[/link]",
            justify="right",
        )
