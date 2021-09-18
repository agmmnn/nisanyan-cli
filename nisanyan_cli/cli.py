# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from urllib.parse import quote
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich import box


def main(word):

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    url = "https://www.nisanyansozluk.com/?k=" + quote(word) + "&lnk=1&view=annotated"
    session.mount(url, adapter)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
        "accept-encoding": "gzip, deflate, br",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "upgrade-insecure-requests": "1",
    }
    try:
        r = session.get(url, headers=headers)
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.TooManyRedirects:
        pass
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"cannot reach nisanyansozluk.com\n{e}")

    soup = BeautifulSoup(r.content, "html5lib")
    div = soup.find("tr", {"class": "yaz hghlght"})

    if div != None:
        for br in div.find_all("br"):
            br.replace_with("\n")
        for s in div.find_all(
            "span", {"style": "display:block;padding-left:25px;font-style:italic;"}
        ):
            s.replace_with("     " + s.text + "\n")
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
        # rich
        table = Table(
            title="[link=" + url + "]" + topic + " - " + "Nişanyan Sözlük[/link]",
            show_header=False,
            box=box.SQUARE,
        )
        table.add_column()
        for idx, i in enumerate(lst):
            newline = "\n" if idx != len(lst) - 1 else ""
            if i[0] != "":
                table.add_row(i[0])
            table.add_row(i[1] + newline)
        Console().print(table, markup=False)

    else:
        print("Sonuç Bulunamadı! Yakın Kelimeler:")
        aa = BeautifulSoup(str(soup.find("tbody")), "lxml").find_all("a")
        wordlist = []
        for i in aa:
            wordlist.append(i.text)
        wordlist.insert(5, "<" + word + ">")
        print(", ".join(wordlist))
        print()
