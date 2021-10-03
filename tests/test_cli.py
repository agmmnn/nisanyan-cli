from nisanyan_cli.cli import Niscli


def test_req():
    assert Niscli("kişi").req().status_code == 200


def test_get_list():
    assert Niscli("kişi").get_list()[1] == "kişi"
    assert Niscli("kişi").get_list()[0][1] == [
        "Köken",
        ' Eski Türkçe kişi  "insan, kimse" sözcüğünden evrilmiştir.',
    ]
    assert Niscli("kişis").get_list() == None


def test_similar_words():
    output = "Sonuç Bulunamadı... Yakın Kelimeler:\nkisra, kist, kisve, kiş, kişi, <kişis>, kişne|mek, kişniş1, kişniş2, kit, kitakse, kitap"
    assert Niscli("kişis").similar_words() == output
