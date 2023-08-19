import pytest

from regex import *


@pytest.mark.parametrize(
    "text, expected_result",
    [("AB12345", True),
     ("aB12345", False),
     ("AA1234", False),
     ("A12345", False)],
)
def test_is_passport_number(text, expected_result):
    assert is_passport_number(text) == expected_result


@pytest.mark.parametrize(
    "text, expected_result",
    [("1234567890", True),
     ("12345", False),
     ("A123456789", False)],
)
def test_is_ipn(text, expected_result):
    assert is_ipn(text) == expected_result


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("AE1234AA", True),
        ("KE1234AA", True),
        ("AX1234AA", False),
        ("ke1234aa", False),
    ],
)
def test_is_car_number_dnipro(text, expected_result):
    assert is_car_number_dnipro(text) == expected_result


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("AX1234AA", True),
        ("KX1234AA", True),
        ("AE1234AB", False),
        ("ax1234BB", False),
    ],
)
def test_is_car_number_kharkiv(text, expected_result):
    assert is_car_number_kharkiv(text) == expected_result