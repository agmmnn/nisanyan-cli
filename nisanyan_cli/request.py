from http.client import HTTPSConnection
from json import loads


def req(word):
    conn = HTTPSConnection("radyal-api.vercel.app")
    conn.request("GET", f"/api/nisanyan-decrypt?word={word}")
    res = conn.getresponse()
    data = res.read()
    return loads(data)
