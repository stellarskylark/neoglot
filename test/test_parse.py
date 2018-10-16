from src import parse
import pytest

def test_parse_def():
    assert parse.parse_def(
        "foo bar: lorem, ipsum, blah, foobar"
    ) == ("foo", "bar", "lorem, ipsum, blah, foobar")

    assert parse.parse_def(
        "aaa bbb :ccc") == ("aaa", "bbb", "ccc")

    with pytest.raises(SystemExit):
        parse.parse_def("aaa: bbb")
    with pytest.raises(SystemExit):
        parse.parse_def(":asdfas")
    with pytest.raises(SystemExit):
        parse.parse_def(":")
    with pytest.raises(SystemExit):
        parse.parse_def("aaaaa")
    with pytest.raises(SystemExit):
        parse.parse_def("foo bar:")

def test_parse_category():
    assert parse.parse_category("a, b, c") == ["a", "b", "c"]

    with pytest.raises(SystemExit):
        parse.parse_category("cat foo: a,, b, c")

    with pytest.raises(SystemExit):
        parse.parse_category("cat foo: a, b c")
