import pathlib
import bencoding


def test_parse_int():
    data = bencoding.decode(b"i42e")
    assert data == 42


def test_parse_dict():
    data = bencoding.decode(b"d3:foo3:bare")
    assert data == {"foo": "bar"}


def test_parse_str():
    data = bencoding.decode(b"4:spam")
    assert data == "spam"


def test_parse_list():
    data = bencoding.decode(b"li1ei2ei3ee")
    assert data == [1, 2, 3]


def test_parse_torrent():
    file = pathlib.Path(__file__).parent / "test_data" / "linuxmint.torrent"
    res = bencoding.decode(file.read_bytes())
    assert isinstance(res, dict)
    assert set(res.keys()) == {
        "announce",
        "created by",
        "creation date",
        "encoding",
        "info",
    }
    assert isinstance(res["info"], dict)
    assert isinstance(res["announce"], str)
    assert isinstance(res["created by"], str)
    assert isinstance(res["creation date"], int)
    assert isinstance(res["encoding"], str)
    assert isinstance(res["info"]["length"], int)
    assert isinstance(res["info"]["name"], str)
    assert isinstance(res["info"]["piece length"], int)
    assert isinstance(res["info"]["pieces"], str)
    assert isinstance(res["info"]["private"], int)
