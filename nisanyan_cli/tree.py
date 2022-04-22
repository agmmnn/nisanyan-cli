from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from rich import print
from rich.tree import Tree
from os import name as os_name
import json


class Nistree:
    def __init__(self, word):
        self.word = word
        if os_name == "nt":
            driver_path = "chromedriver.exe"
        else:
            driver_path = "chromedriver"
        self.url = f"https://www.nisanyansozluk.com/kelime/{quote(word)}"
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        try:
            self.driver = webdriver.Chrome(driver_path, options=options)
        except Exception as e:
            print(e)
            exit(1)
        self.driver.get(self.url)
        # wait
        try:
            WebDriverWait(self.driver, 3).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, ".sc-7f314b79-12")
                )
            )
        except:
            aa = [
                i.text
                for i in self.driver.find_element(
                    By.CSS_SELECTOR, ".sc-c67120d4-1.cxEZrH"
                ).find_elements(By.TAG_NAME, "a")
            ]
            print(", ".join(aa[:-1]))
            self.driver.quit()
            exit()
        # click kompakt buton
        kompakt_buton = self.driver.find_element(
            By.XPATH, "(//div[@class='react-switch-bg'])[1]"
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", kompakt_buton)
        self.driver.execute_script("arguments[0].click();", kompakt_buton)
        with open("nisanyan_cli/langs.json", "r", encoding="utf-8") as f:
            self.lang_dict = json.load(f)
        self.get_data()
        self.driver.quit()

    def print_data(self, data):
        lst = []
        for i in data["nodes"]:
            lst.append(
                i["word"]
                + (f"({i['word_orj']})" if i["word_orj"] != "" else "")
                + (
                    f' ([cyan]{i["dil"]})'
                    if i["dil"] not in self.lang_dict
                    else (
                        f' [cyan]([link={self.lang_dict[i["dil"]]["wiki_link"]}]'
                        + self.lang_dict[i["dil"]]["name"]
                        + "[/link]"
                        + f' {self.lang_dict[i["dil"]]["era"]})'  # 🏛️
                    )
                )
                + (f': [gray70]{i["anlam"]}.[/gray70]' if i["anlam"] != "" else "")
            )

        tree = Tree(f'{data["name"]} [cyan](Günümüz Türkçesi)')
        sub = {}
        sub[lst[0]] = tree.add(lst[0])
        last1 = sub[lst[0]]
        if len(lst) > 1:
            for ix, i in enumerate(lst[1:]):
                if data["nodes"][ix + 1]["type"] == 1:
                    sub[i] = sub[list(sub.keys())[-1]].add(i)
                    last1 = sub[list(sub.keys())[-1]]
                if data["nodes"][ix + 1]["type"] == 2:
                    sub[i] = last1.add(i)

        print(tree)
        print()

    def get_data(self):
        data = {}
        divs = self.driver.find_elements(By.CSS_SELECTOR, ".sc-7f314b79-0")
        for ix, i in enumerate(divs):
            idx = ix + 1
            # Kelime başlığı
            kelime_baslik = i.find_element(By.CSS_SELECTOR, ".sc-7f314b79-2").text
            # Köken
            koken = i.find_element(By.CSS_SELECTOR, ".sc-7f314b79-11.ctVVLQ")
            spans = koken.find_elements(By.XPATH, "./child::*")
            data_types = [
                "birleşik kelime",
                "bileşik sözcük",
                "bileşik sözcüğün devamı",
            ]
            nodes = []
            for i in spans:
                dil, tip, word, word_orj, anlam = "", 1, "", "", ""
                for elem in i.find_elements(By.XPATH, "./child::*"):
                    if elem.get_attribute("data-tip") in data_types:
                        tip = 2
                    elif elem.get_attribute("style") == "font-weight: 700;":
                        dil = elem.get_attribute("data-tip")
                    elif (
                        elem.get_attribute("style")
                        == 'font-style: italic; font-family: Tahoma, -apple-system, "Helvetica Neue", Helvetica, Roboto, sans-serif;'
                    ):
                        word = elem.text
                    elif elem.get_attribute("dir") == "rtl":
                        word_orj = elem.text
                    elif (
                        (elem.text != "(")
                        and (elem.text != ")")
                        and (elem.text != "a.a.")
                        and ("sc-7f314b79-15" not in elem.get_attribute("class"))
                    ):
                        if elem.tag_name == "a":
                            anlam = (
                                f'\[[link={elem.get_attribute("href")}]{elem.text}[/link]] '
                                + anlam
                            )
                        else:
                            anlam = elem.text

                nodes.append(
                    {
                        "dil": dil,
                        "type": tip,
                        "word": word,
                        "word_orj": word_orj,
                        "anlam": anlam,
                    }
                )
            data = {"name": kelime_baslik, "nodes": nodes}
            self.print_data(data)
