from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.align import Align
from os import name as os_name


class Niscli:
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

        try:
            WebDriverWait(self.driver, 6).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, ".sc-7f314b79-12")
                )
            )
        except:
            print("error")
            exit()

        data = self.get_data()
        self.print_data(data)
        self.driver.quit()

    def print_data(self, data):
        # print(data)
        for i in data:
            table = Table(box=box.ROUNDED, show_footer=True)
            table.add_column(
                i,
                header_style="bold",
                footer=Align(
                    data[i]["son_guncelleme"],
                    vertical="middle",
                    align="right",
                    style="grey27",
                ),
            )
            table.add_row("[#994E8E]Köken:[/#994E8E]\n" + data[i]["koken"] + "\n")
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
                + ", ".join(data[i]["bu_maddeye_gonderenler"])
                + "\n"
            ) if data[i]["bu_maddeye_gonderenler"] else None
            table.add_row(
                "[#994E8E]Tarihçe: (tespit edilen en eski Türkçe kaynak ve diğer örnekler)[/#994E8E]\n"
                + "\n".join(data[i]["tarihce"])
            ) if data[i]["tarihce"] else None
            print(table)
        Console().print(
            f"[grey42][link={self.url}]nisanyansozluk.com↗[/link]", justify="right"
        )

    def get_data(self):
        data = {}
        divs = self.driver.find_elements(By.CSS_SELECTOR, ".sc-7f314b79-0")
        for ix, i in enumerate(divs):
            idx = ix + 1
            # Kelime başlığı
            kelime_baslik = i.find_element(By.CSS_SELECTOR, ".sc-7f314b79-2").text
            try:
                # Köken
                koken = i.find_element(
                    By.CSS_SELECTOR,
                    ".sc-7f314b79-12",
                ).text.strip()
            except:
                koken = ""
            # Daha fazla bilgi için .. maddesine bakınız.
            try:
                daha_fazla = i.find_element(
                    By.CSS_SELECTOR,
                    ".sc-7f314b79-12>div",
                )
                koken = koken.replace(daha_fazla.text, "").strip()
                daha_fazla = [
                    i.text for i in daha_fazla.find_elements(By.TAG_NAME, "a")
                ]
            except:
                daha_fazla = []
            # Ek açıklama
            try:
                ek_aciklama = i.find_element(
                    By.XPATH,
                    f"(//div[normalize-space()='Ek açıklama']/following-sibling::div)[{idx}]",
                ).text
            except:
                ek_aciklama = ""
            # Benzer sözcükler
            try:
                benzer_sozcukler = i.find_element(
                    By.XPATH,
                    f"(//div[normalize-space()='Benzer sözcükler']/following-sibling::div)[{idx}]",
                ).text.split(", ")
            except:
                benzer_sozcukler = []
            # Bu maddeye gönderenler
            try:
                bu_maddeye_gonderenler = i.find_element(
                    By.XPATH,
                    f"(//div[normalize-space()='Bu maddeye gönderenler']/following-sibling::div)[{idx}]",
                ).find_elements(By.TAG_NAME, "a")
                bu_maddeye_gonderenler = [i.text for i in bu_maddeye_gonderenler]
            except:
                bu_maddeye_gonderenler = []
            # Tarihçe
            try:
                tarihce = i.find_element(
                    By.XPATH,
                    f"(//span[contains(text(),'(tespit edilen en eski Türkçe kaynak ve diğer örnekler)')]/../following-sibling::div)[{idx}]",
                ).find_elements(By.CSS_SELECTOR, ".sc-7f314b79-16")
                tarihcelist = []
                for k in tarihce:
                    j = k.find_elements(By.CSS_SELECTOR, "div")
                    tarihcelist.append(
                        "[gray58]"
                        + j[0].text.replace("[", "\[")
                        + "[/gray58]\n  "
                        + j[1].text
                    )
                tarihce = tarihcelist
            except:
                tarihce = []
            # Son güncelleme
            son_guncelleme = i.find_element(By.CLASS_NAME, "sc-7f314b79-24").text

            data[kelime_baslik] = {
                "koken": koken,
                "daha_fazla": daha_fazla,
                "ek_aciklama": ek_aciklama,
                "benzer_sozcukler": benzer_sozcukler,
                "bu_maddeye_gonderenler": bu_maddeye_gonderenler,
                "tarihce": tarihce,
                "son_guncelleme": son_guncelleme,
            }
        return data
