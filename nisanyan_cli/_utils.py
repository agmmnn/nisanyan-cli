import re


def replace_chars(text):
    text = (
        text.replace("%b", "")
        .replace("%i", "")
        .replace("%u", "")
        .replace("%l", "")
        .replace("%r", "")
    )

    replacements = {
        "ETü": "Eski Türkçe",
        "a.a.": "aynı anlam",
        "Yun": "Yunanca",
        "Lat": "Latince",
        "Ar": "Arapça",
        "Far": "Farsça",
        "Fa": "Farsça",
        "Fr": "Fransızca",
        "İng": "İngilizce",
        "Tr": "Türkçe",
        "Erm": "Ermenice",
        "Osm": "Osmanlıca",
        "Sür": "Süryanice",
        "İbr": "İbranice",
        "Sans": "Sanskritçe",
        "Alm": "Almanca",
        "İt": "İtalyanca",
        "Moğ": "Moğolca",
        "Rum": "Rumca",
        "Eth": "Etiyopça",
        "TTü": "Türkiye Türkçesi",
        "YTü": "Yeni Türkçe",
    }

    for k, v in replacements.items():
        pattern = r"(?<!\w)" + re.escape(k) + r"(?!\w)"
        text = re.sub(pattern, v, text)

    return text


def date_convert(date):
    aylar = {
        "01": "Ocak",
        "02": "Şubat",
        "03": "Mart",
        "04": "Nisan",
        "05": "Mayıs",
        "06": "Haziran",
        "07": "Temmuz",
        "08": "Ağustos",
        "09": "Eylül",
        "10": "Ekim",
        "11": "Kasım",
        "12": "Aralık",
    }
    date = date.split("-")
    return date[2] + " " + aylar[date[1]] + " " + date[0]
