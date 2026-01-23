from http.client import HTTPSConnection
from json import loads, JSONDecodeError
import sys


def req(path, host="www.nisanyansozluk.com"):
    conn = HTTPSConnection(host)
    conn.request("GET", f"{path}?session=1")
    res = conn.getresponse()
    data = res.read()
    try:
        return loads(data)
    except JSONDecodeError:
        sys.stderr.write(
            f"Error: Could not retrieve data from {host}. The API might have changed or the resource was not found.\n"
        )
        sys.exit(1)
