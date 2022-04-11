# -*- coding: utf-8 -*-
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from rich.table import Table
from rich.markup import escape
from rich import box
from rich import print as rprint


class Niscli:
    def __init__(self, word):
        self.word = word
        self.url = "https://www.nisanyansozluk.com/kelime/{}"
        self.req()

    def req(self):
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        }

        try:
            r = session.get(self.url.format(quote(self.word)), headers=headers)
        except requests.exceptions.Timeout as e:
            raise SystemExit(e)
        except requests.exceptions.TooManyRedirects as e:
            raise SystemExit(e)
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"cannot reach nisanyansozluk.com\n{e}")

        self.soup = BeautifulSoup(r.content, "lxml")
        return r

    def similar_words(self):
        aa = BeautifulSoup(str(self.soup.find("tbody")), "lxml").find_all("a")
        wordlist = []
        for i in aa:
            wordlist.append(i.text)
        wordlist.insert(5, "<" + self.word + ">")
        return "Sonuç Bulunamadı... Yakın Kelimeler:\n" + ", ".join(wordlist)

    def get_list(self):

        rprint(self.soup)
        div = self.soup.find("div", {"class": "sc-6f05a3c6-2 chGjLE"})
        print(div)
        # if div is None:
        #     print(self.similar_words())
        #     return None
        return None

        for br in div.find_all("br"):
            br.replace_with("\n")
        for s in div.find_all(
            "span", {"style": "display:block;padding-left:25px;font-style:italic;"}
        ):
            s.replace_with("\n     > " + s.text + "\n")
        topic = div.a.text.strip()
        resultsoup = BeautifulSoup(str(div), "lxml")
        results = resultsoup.find_all("div", {"class": "eskoken"})
        lst = []
        for i in results:
            if i.find("div", class_="blmbasi") is not None:
                lst.append(
                    [
                        i.find("div", class_="blmbasi").text.strip(),
                        " " + i.p.get_text().replace("[ ", "[").strip(),
                    ]
                )
            else:
                lst.append(["", i.p.text.strip()])
        return lst, topic

    def rich_output(self):
        list = self.get_list()
        if list is None:
            exit()
        lst = list[0]
        topic = list[1]
        table = Table(
            title="[green][link="
            + self.url.format(quote(self.word))
            + "]"
            + topic
            + " - "
            + "Nişanyan Sözlük[/link]",
            show_header=False,
            box=box.SQUARE,
        )
        table.add_column()
        for idx, i in enumerate(lst):
            newline = "\n" if idx != len(lst) - 1 else ""
            if i[0] != "":
                table.add_row("[cyan]" + i[0])
            table.add_row(escape(i[1]) + newline)
        rprint(table)

    def plain_output(self):
        list = self.get_list()
        if list is None:
            exit()
        lst = list[0]
        topic = list[1]
        print(topic)
        for idx, i in enumerate(lst):
            newline = "\n" if idx != len(lst) - 1 else ""
            if i[0] != "":
                print(i[0] + ":")
            print(i[1] + newline)
