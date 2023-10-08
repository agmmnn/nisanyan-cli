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
    conn.request("GET", f"/api/names/{name}?session=1")
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
            self.name = self.data["randomName"].capitalize()
            self.data = req(quote(self.name))
        elif self.name == "nonexistname":
            exit(1)
        elif not self.data["isSuccessful"]:
            print("Not found!")
            exit(1)

        self.rich_output()

    def rich_output(self):
        for i in self.data["names"]:
            # gender
            gender_ratio = i["genderRatio"]
            female_percentage = gender_ratio * 100
            male_percentage = (1 - gender_ratio) * 100
            gender = f"[pink1]\u2640:{male_percentage:.0f}%[/] [deep_sky_blue1]\u2642:{female_percentage:.0f}% [/]"

            # years
            # Initialize decade counts
            decade_counts = {}
            for year in range(1950, 2030, 10):
                decade_counts[f"{year}s"] = 0

            year_data = {}
            for variant in i["variants"]:
                if i["name"] == variant["name"]:
                    year_data = variant["years"]

            # Count the popularity for each decade
            for year, count in year_data.items():
                year = int(year)
                if year >= 1950 and year < 2030:
                    decade = ((year - 1950) // 10) * 10 + 1950
                    decade_counts[f"{decade}s"] += count

            years = []
            for decade, count in decade_counts.items():
                years.append(f"{decade[-3:]}: {count}")

            table = Table(box=box.ROUNDED, show_footer=True, expand=True)
            table.add_column(
                f'{i["name"]} {gender} [pale_green1]{i["count"]} kişi:[/] [gray19]{", ".join(years)}[/]',
                header_style="bold",
                footer=Align(
                    f'sıklık sırası: {i["rank"]}',
                    vertical="middle",
                    align="center",
                    style="grey42",
                ),
            )
            # cache["nations"] nat_code=yt : cache["languages"] lang_code:t
            table.add_row(
                "[#994E8E]Köken:[/#994E8E]" + "\n" + i["definition"] + "\n"
            ) if i["definition"] else None
            table.add_row((i["note"]) + "\n") if i["note"] else None
            # 0: ulusal t: türkçe alanı
            table.add_row(
                "[#994E8E]Dağılım:[/#994E8E]"
                + "\n"
                + (
                    ", ".join(j["name"] for j in i["region"]["locations"])
                    if i["region"]["locations"] != []
                    else "Ulusal"
                )
                + "\n"
            )
            table.add_row(
                "[#994E8E]Farklı Yazılışlar: (Alfabetik)[/#994E8E]"
                + "\n"
                + ", ".join(
                    [f'{j["name"]} ({j["count"]["total"]})' for j in i["variants"]]
                )
            ) if i["variants"] else None
            table.add_row(
                "[#994E8E]İlgili Adlar:[/#994E8E]" + "\n" + ", ".join(i["relatedNames"])
            ) if i["relatedNames"] else None

            print(table)
        Console().print(
            f"[grey42][link=https://www.nisanyanadlar.com/isim/{quote(self.name)}]nisanyanadlar.com/isim/{self.name}↗[/link]",
            justify="right",
        )
