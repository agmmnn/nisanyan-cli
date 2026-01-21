from rich import box, print
from rich.align import Align
from rich.console import Console
from rich.table import Table
from urllib.parse import quote
from .request import req
import sys


class Nisadlar:
    def __init__(self, name, random: bool = False):
        self.name = name
        self.random = random
        self.data = None

    def run(self):
        self.fetch_data()
        self.display()

    def fetch_data(self):
        if not self.name and not self.random:
            self.name = "nonexistname"

        if self.name:
            self.name = self.name.capitalize()
        else:
            self.name = "nonexistname"

        self.data = req(f"/api/names/{quote(self.name)}", host="www.nisanyanadlar.com")

        if self.random and self.data and "randomName" in self.data:
            self.name = self.data["randomName"].capitalize()
            self.data = req(
                f"/api/names/{quote(self.name)}", host="www.nisanyanadlar.com"
            )

    def display(self):
        if not self.data:
            return

        if not self.data.get("isSuccessful"):
            print("Not found!")
            sys.exit(1)

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

            if i["definition"]:
                table.add_row(
                    "[#994E8E]Köken:[/#994E8E]" + "\n" + i["definition"] + "\n"
                )
            if i["note"]:
                table.add_row((i["note"]) + "\n")

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

            if i["variants"]:
                table.add_row(
                    "[#994E8E]Farklı Yazılışlar: (Alfabetik)[/#994E8E]"
                    + "\n"
                    + ", ".join(
                        [f'{j["name"]} ({j["count"]["total"]})' for j in i["variants"]]
                    )
                )

            if i["relatedNames"]:
                table.add_row(
                    "[#994E8E]İlgili Adlar:[/#994E8E]" + "\n" + ", ".join(i["relatedNames"])
                )

            print(table)
        Console().print(
            f"[grey42][link=https://www.nisanyanadlar.com/isim/{quote(self.name)}]nisanyanadlar.com/isim/{self.name}↗[/link]",
            justify="right",
        )
