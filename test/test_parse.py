from src import parse
import pytest

def test_parse_def():
    assert parse.parse_def(
        "foo bar: lorem, ipsum, blah, foobar"
    ) == ("foo", "bar", "lorem, ipsum, blah, foobar")

    assert parse.parse_def(
        "aaa bbb :ccc") == ("aaa", "bbb", "ccc")

    # no identifier
    with pytest.raises(SystemExit):
        parse.parse_def("aaa: bbb")
    # no prefix
    with pytest.raises(SystemExit):
        parse.parse_def(":asdfas")
    # nothing but colon
    with pytest.raises(SystemExit):
        parse.parse_def(":")
    # no semicolon or prefix
    with pytest.raises(SystemExit):
        parse.parse_def("aaaaa")
    # no definition after prefix
    with pytest.raises(SystemExit):
        parse.parse_def("foo bar:")

def test_parse_category():
    assert parse.parse_category("a, b, c") == ["a", "b", "c"]

    # extra semicolon
    with pytest.raises(SystemExit):
        parse.parse_category("a,, b, c")
    # missing semicolon
    with pytest.raises(SystemExit):
        parse.parse_category("a, b c")

def test_pull_elements():
    assert parse.pull_elements(
        "[a] (b) [c] (d)") == ['[a]', '(b)', '[c]', '(d)']

    # nested elements are disallowed
    with pytest.raises(SystemExit):
        parse.parse_category("(a | (b))[c]")
    # unbalanced parentheses/brackets
    with pytest.raises(SystemExit):
        parse.parse_category("[a]((b)")
    with pytest.raises(SystemExit):
        parse.parse_category("[[a](b)")
