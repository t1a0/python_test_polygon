from drunk_polish_calculator import *
import pytest


def test_op_plus():
    x = 3
    y = 2
    expected_result = 5
    assert expected_result == op_plus(x, y)


def test_op_minus():
    x = 3
    y = 2
    expected_result = 1
    assert expected_result == op_minus(x, y)


def test_op_multiply():
    x = 3
    y = 2
    expected_result = 6
    assert expected_result == op_multiply(x, y)


def test_op_divide():
    x = 6
    y = 2
    expected_result = 3
    assert expected_result == op_divide(x, y)


def test_main(capsys, monkeypatch):
    input_string = "2 3 + 1 - 3 * 3 / "
    expected_output = "4.0\n"

    monkeypatch.setattr("builtins.input", lambda _: input_string)

    main()

    output = capsys.readouterr().out
    assert output == expected_output
