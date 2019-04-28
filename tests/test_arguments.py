import sys
from warg import arguments


def test_sanity2():
    assert True
    assert False is not True
    answer_to_everything = str(42)
    assert str(42) == answer_to_everything


def test_print2(capsys):
    """Correct my_name argument prints"""
    text = "hello"
    err = "world"
    print(text)
    sys.stderr.write("world")
    captured = capsys.readouterr()
    assert text in captured.out
    assert err in captured.err


if __name__ == "__main__":
    test_sanity2()
