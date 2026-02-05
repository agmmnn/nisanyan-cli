from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.align import Align
from urllib.parse import quote
from ._utils import replace_chars, date_convert

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
    def __init__(self, word, request, plain=False):
        self.word = word
        self.request = request
        self.plain = plain

    def display(self):
        if self.plain:
            self.print_plain()
        else:
            self.print_rich()

    def get_data(self):
        output = {}
        data = self.request
        words = data.get("words", [])

        for i in words:
            # Köken
            try:
                lst = []
                koken = ""
                etymologies = i.get("etymologies", [])
                for j in etymologies:
                    languages = j.get("languages", [])
                    lang_name = languages[0]["name"] if languages else ""

                    romanized = j.get("romanizedText", "")
                    original = j.get("originalText", "")
                    definition = j.get("definition", "")

                    txt = (
                        f'[b]{lang_name}[/] [i]{romanized}[/] {(original+" " if original else "")}'
                        + ("“" + definition + "”" if definition else "")
                    )
                    lst.append(txt)
                for j in lst:
                    koken = koken + j + ". "
            except (KeyError, IndexError):
                koken = None

            # Daha fazla
            try:
                daha_fazla = [j["name"] for j in i.get("references", [])]
            except (KeyError, TypeError):
                daha_fazla = []

            # Bu maddeye gönderenler
            try:
                maddeye_gonderenler = [j["name"] for j in i.get("referenceOf", [])]
            except (KeyError, TypeError):
                maddeye_gonderenler = []

            # Tarihçe
            try:
                lst = []
                tarihce = ""
                histories = i.get("histories", [])
                for j in histories:
                    language = j.get("language", {})
                    lang_name = language.get("name") if language else ""

                    definition = j.get("definition", "")
                    excerpt = j.get("excerpt", "")
                    source = j.get("source", {})
                    source_name = source.get("name", "")
                    source_book = source.get("book", "")
                    date = j.get("date", "")

                    txt = (
                        (f'{lang_name}: ' if lang_name else "")
                        + (f'"{definition}" ' if definition else "")
                        + (f'[i]{excerpt}[/] ' if excerpt else "")
                        + f'[grey50][{(source_name+", ") if source_name else ""}{source_book}, {date}][/]'
                    )

                    quote_text = j.get("quote", "")
                    quote_val = replace_chars(
                        quote_text.replace("[", "〔").replace("]", "〕")
                    )
                    lst.append([txt, quote_val])

                for j_idx, j in enumerate(lst):
                    tarihce = (
                        tarihce
                        + j[0]
                        + (f"\n  [i]{j[1]}[/]" if j[1] else "")
                        + ("\n" if j_idx != len(lst) - 1 else "")
                    )
            except (KeyError, IndexError, TypeError):
                tarihce = None

            time_updated = i.get("timeUpdated", "")
            son_guncelleme = date_convert(time_updated[:10]) if time_updated else ""

            output[i["name"]] = {
                "koken": replace_chars(koken) if koken else None,
                "daha_fazla": daha_fazla,
                "ek_aciklama": replace_chars(i.get("note", "")) if i.get("note") else None,
                "benzer_sozcukler": i.get("similarWords", []),
                "maddeye_gonderenler": maddeye_gonderenler,
                "tarihce": tarihce,
                "son_guncelleme": son_guncelleme,
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
                    data[i].get("son_guncelleme", ""),
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
