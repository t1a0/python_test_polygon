from drunk_polish_calculator import *
import pytest


@pytest.mark.parametrize(
    "x, y, expected_result",
    [
        (3, 2, 5),
        (-3, 2, -1),
        (3, -2, 1),
        (-3, -2, -5),
        (3.5, 2, 5.5),
        (3, 2.5, 5.5),
        (3.5, 2.5, 6),
    ],
)
def test_op_plus(x, y, expected_result):
    assert op_plus(x, y) == expected_result


@pytest.mark.parametrize(
    "x, y, expected_error",
    [("3", 2, TypeError), (3, "2", TypeError), ((3, 3), 2, TypeError)],
)
def test_error_op_plus(x, y, expected_error):
    with pytest.raises(expected_error):
        assert op_plus(x, y) == expected_error


@pytest.mark.parametrize(
    "x, y, expected_result",
    [
        (3, 2, 1),
        (2, 3, -1),
        (-3, 2, -5),
        (-3, -2, -1),
        (-3.5, -2, -5.5),
        (-3, 2.5, -5.5),
        (-3.5, -2.5, -6),
    ],
)
def test_op_minus(x, y, expected_result):
    assert op_minus(x, y) == expected_result


@pytest.mark.parametrize(
    "x, y, expected_error",
    [("3", 2, TypeError), (3, "2", TypeError), ((3, 3), 2, TypeError)],
)
def test_error_op_minus(x, y, expected_error):
    with pytest.raises(expected_error):
        op_minus(x, y)


@pytest.mark.parametrize(
    "x, y, expected_result",
    [
        (3, 2, 6),
        (-3, 2, -6),
        (3, -2, -6),
        (-3, -2, 6),
        (3.5, 2, 7),
        (3, 2.5, 7.5),
        (3.5, 2.5, 8.75),
    ],
)
def test_op_multiply(x, y, expected_result):
    assert op_multiply(x, y) == expected_result


@pytest.mark.parametrize(
    "x, y, expected_result",
    [
        (4, 2, 2),
        (0, 2, 0),
        (4, -2, -2),
        (-4, 2, -2),
        (-4, -2, 2),
        (5.5, 2, 2.75),
        (5.5, 2.5, 2.2),
    ],
)
def test_op_divide(x, y, expected_result):
    assert op_divide(x, y) == expected_result


@pytest.mark.parametrize(
    "x, y, expected_error",
    [
        ("3", 2, TypeError),
        (3, "2", TypeError),
        (3, 0, ZeroDivisionError),
        ("2", "3", TypeError),
        ((2, 3), -3, TypeError),
    ],
)
def test_error_op_divide(x, y, expected_error):
    with pytest.raises(expected_error):
        op_divide(x, y)


@pytest.mark.parametrize(
    "value, expected_result",
    [
        ("3 2 +", "5.0"),
        ("3 2 -", "1.0"),
        ("3 2 *", "6.0"),
        ("6 2 /", "3.0"),
        ("3 2 + 1 +", "6.0"),
        ("3 2 + 1 -", "2.0"),
        ("3 2 + 1 - 4 * ", "1.0"),
        ("3 2 + 1 - 4 * 2 /", "3.0"),
    ],
)
def test_main(monkeypatch, capsys, value, expected_result):
    monkeypatch.setattr("builtins.input", lambda _: value)

    main()

    result = capsys.readouterr().out
    assert result == (expected_result + "\n")
