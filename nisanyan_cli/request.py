from http.client import HTTPSConnection
from json import loads


def req(word):
    conn = HTTPSConnection("www.nisanyansozluk.com")
    conn.request("GET", f"/api/words/{word}?session=1")
    res = conn.getresponse()
    data = res.read()
    return loads(data)
