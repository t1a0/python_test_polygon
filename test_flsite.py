import datetime
import requests
from requests import Session

import flsite
from config import host, user, password, db_name
from bank_card_repository import BankCardRepository
import pytest
import psycopg2
from bs4 import BeautifulSoup


# ---------------------------------------------------UNIT-тести-------------------------------------------------------
@pytest.mark.parametrize(
    "number, expected_result",
    [
        ("1234567890123456", False),
        ("1234-5678-9012-3456", False),
        ("123456789012345", True),
        ("abcdefghijabcdefgh", True),
        ("123456789012345a", True),
    ],
)
def test_check_number(number, expected_result):
    assert flsite.check_number(number) == expected_result


@pytest.mark.parametrize(
    "exp_date, expected_result",
    [
        ("12/2023", False),
        ("06/2025", False),
        ("13/2024", True),
        ("00/0000", True),
        ("01/4045", False),
        ("0123", True),
    ],
)
def test_check_exp_date(exp_date, expected_result):
    assert flsite.check_exp_date(exp_date) == expected_result


@pytest.mark.parametrize(
    "date, expected_result",
    [
        ("2022-05-15", False),
        ("2021-12-31", False),
        ("2023-13-01", True),
        ("2020-00-00", True),
        ("2023-01-45", True),
        ("2023-02", True),
        ("20230515", False),
    ],
)
def test_check_issue_date(date, expected_result):
    assert flsite.check_issue_date(date) == expected_result


import pytest


@pytest.mark.parametrize(
    "cvv, expected_result",
    [
        ("123", False),
        ("999", False),
        ("1234", True),
        ("abc", True),
        ("12", True),
        ("000", False),
    ],
)
def test_check_cvv(cvv, expected_result):
    assert flsite.check_cvv(cvv) == expected_result


# ---------------------------------------------------Інтеграційні тесты--------------------------------------------------
def clear_a_table():
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    cursor = connection.cursor()

    cursor.execute("DELETE FROM cards")
    connection.commit()


def prepare_a_table():
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    connection.autocommit = True
    clear_a_table()
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS cards(
                                card_number BIGINT PRIMARY KEY NOT NULL,
                                card_exp_date DATE NOT NULL,
                                card_cvv INT NOT NULL,
                                card_issue_date DATE NOT NULL,
                                card_user_id UUID NOT NULL,
                                card_status VARCHAR(20));"""
    )
    cursor.execute(
        """INSERT INTO cards VALUES (4444222244442222, '2023-06-01', 333,
                    '2025-04-21', 'b88603d9-91f6-4e7b-a088-d746e75e07f1', 'new');"""
    )
    return


prepare_a_table()


@pytest.mark.parametrize(
    "number, exp_date, cvv, issue_date, expected_result",
    [
        (
            4444222244442222,
            "06/2023",
            333,
            "2025-04-21",
            "Така картка вже існує!",
        ),
        (
            1234,
            "06/2023",
            333,
            "2025-04-21",
            "Невірний номер !",
        ),
        (
            4444222244442222,
            "26/2023",
            333,
            "2025-04-21",
            "Невірна дата кінцевого строку дії !",
        ),
        (
            4444222244442222,
            "11/2023",
            1,
            "2025-04-21",
            "Невірний cvv !",
        ),
        (
            4444222244442222,
            "11/2023",
            333,
            "2025-24-21",
            "Невірна дата випуску !",
        ),
    ],
)
def test_create_card_error(number, exp_date, cvv, issue_date, expected_result):
    url = r"http://127.0.0.1:5000/create"
    data = {
        "number": number,
        "exp_date": exp_date,
        "cvv": cvv,
        "issue_date": issue_date,
    }

    con = Session()
    temp = con.post(url, data=data)
    soup = BeautifulSoup(temp.text, "lxml")
    result = soup.find("p", class_="error").text
    con.close()

    assert result == expected_result


@pytest.mark.parametrize(
    "number, exp_date, cvv, issue_date, expected_result",
    [
        (
            4444222244442221,
            "06/2023",
            333,
            "2025-04-21",
            "Додано нову банківську картку!",
        ),
    ],
)
def test_create_card_success(number, exp_date, cvv, issue_date, expected_result):
    url = r"http://127.0.0.1:5000/create"
    data = {
        "number": number,
        "exp_date": exp_date,
        "cvv": cvv,
        "issue_date": issue_date,
    }

    con = Session()
    temp = con.post(url, data=data)
    soup = BeautifulSoup(temp.text, "lxml")
    result = soup.find("p", class_="success").text
    con.close()

    assert result == expected_result


@pytest.mark.parametrize(
    "number, expected_result",
    [
        (
            4444222244442222,
            """[(4444222244442222,datetime.date(2023,6,1),333,datetime.date(2025,4,21),'b88603d9-91f6-4e7b-a088-d746e75e07f1','new')]""",
        ),
        (1111222233334445, "[]"),
    ],
)
def test_check_success(number, expected_result):
    url = "http://127.0.0.1:5000/check"
    data = {
        "number": number,
    }
    con = Session()
    temp = con.post(url, data=data)
    soup = BeautifulSoup(temp.text, "lxml")
    result = soup.find("div", class_="result").text
    con.close()
    assert expected_result == result.replace("\n", "").replace(" ", "").replace(
        "\t", ""
    )


@pytest.mark.parametrize(
    "number, expected_result",
    [
        (1111222, "Невірний номер !"),
    ],
)
def test_check_error(number, expected_result):
    url = "http://127.0.0.1:5000/check"
    data = {
        "number": number,
    }
    con = Session()
    temp = con.post(url, data=data)
    soup = BeautifulSoup(temp.text, "lxml")
    result = soup.find("p", class_="error").text
    con.close()
    assert expected_result == result
