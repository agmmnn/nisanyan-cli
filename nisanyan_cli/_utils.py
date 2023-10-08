def replace_chars(text):
    return (
        text.replace("%b", "")
        .replace("%i", "")
        .replace("%u", "")
        .replace("%l", "")
        .replace("ETü", "Eski Türkçe")
        .replace("a.a.", "aynı anlam")
    )


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
