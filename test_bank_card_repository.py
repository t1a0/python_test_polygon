import datetime

from config import host, user, password, db_name
from bank_card_repository import BankCardRepository
from bank_card import Card
from uuid import uuid4
import pytest
import psycopg2


def prepare_a_table():
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    connection.autocommit = True
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
    return


def clear_a_table():
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    cursor = connection.cursor()

    cursor.execute("DELETE FROM cards")
    connection.commit()


prepare_a_table()


@pytest.mark.parametrize(
    "old_date, expected_result", [("11/2023", "2023-11-01"), ("10/2020", "2020-10-01")]
)
def test_correct_date(old_date, expected_result):
    date_test = BankCardRepository(host, user, password, db_name)
    assert date_test.correct_date(old_date) == expected_result


@pytest.mark.parametrize(
    "old_status, new_status, expected_result",
    [
        ("active", "new", "new"),
        ("active", "blocked", "blocked"),
        ("new", "active", "active"),
        ("new", "blocked", "blocked"),
    ],
)
def test_card_status(old_status, new_status, expected_result):
    card1 = Card(
        1234_5678_9012_0000, "01/2023", 123, "2028-01-01", str(uuid4()), old_status
    )
    card1.status = new_status
    assert card1.status == expected_result


@pytest.mark.parametrize(
    "old_status, new_status, expected_exception",
    [
        ("blocked", "active", ValueError),
        ("blocked", "new", ValueError),
        ("active", "dead", ValueError),
    ],
)
def test_card_status_error(old_status, new_status, expected_exception):
    card1 = Card(
        1234_5678_9012_0000, "01/2023", 123, "2028-01-00", str(uuid4()), old_status
    )
    with pytest.raises(expected_exception):
        card1.card_status = new_status


def expected_result_for_get():
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(
        """SELECT EXISTS (SELECT * FROM cards WHERE card_number = 1111222233334444);"""
    )
    check = cursor.fetchone()

    if check == False:
        cursor.execute(
            """INSERT INTO cards VALUES (1111222233334444, '2023-01-01', 123,
            '2028-01-01', 'b88603d9-91f6-4e7b-a088-d746e75e07f1', 'active');"""
        )

    cursor.execute("""SELECT * FROM cards WHERE card_number = 1111222233334444""")

    expected_result = cursor.fetchone()

    return expected_result


def test_get():
    func_test = BankCardRepository(host, user, password, db_name)
    expected_result = expected_result_for_get()
    result = func_test.get(1111222233334444)
    assert result[0] == expected_result


def expected_result_for_save():
    connnection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    cursor = connnection.cursor()

    cursor.execute("SELECT * FROM cards")
    expected_result = cursor.fetchone()
    cursor.close()
    connnection.close()
    return expected_result


def test_save():
    clear_a_table()
    func_test = BankCardRepository(host, user, password, db_name)
    card = Card(
        1111_2222_3333_4444,
        "01/2022",
        123,
        "2028-01-01",
        "fdd348f9-438c-4cd5-996d-e04de0019bd1",
        "active",
    )

    func_test.save(card)

    result = expected_result_for_save()

    assert result == (
        1111_2222_3333_4444,
        datetime.date(2022, 1, 1),
        123,
        datetime.date(2028, 1, 1),
        "fdd348f9-438c-4cd5-996d-e04de0019bd1",
        "active",
    )


def expected_result_for_find_by_exp_date():
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cards WHERE card_exp_date = '2022-01-01'")

    expected_result = cursor.fetchone()

    return expected_result


def test_find_by_exp_date():
    func_test = BankCardRepository(host, user, password, db_name)
    expected_result = expected_result_for_find_by_exp_date()
    result = func_test.find_by_exp_date("01/2022")
    assert result[0] == expected_result


def expected_result_for_find_by_issue_date():
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cards WHERE card_issue_date = '2028-01-01'")

    expected_result = cursor.fetchone()

    return expected_result


def test_find_by_issue_date():
    func_test = BankCardRepository(host, user, password, db_name)
    expected_result = expected_result_for_find_by_exp_date()
    result = func_test.find_by_issue_date("2028-01-01")
    assert result[0] == expected_result


def expected_result_for_find_by_uuid():
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=db_name
    )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM cards WHERE card_uuid = 'fdd348f9-438c-4cd5-996d-e04de0019bd1'"
    )

    expected_result = cursor.fetchone()

    return expected_result


def test_find_by_uuid():
    func_test = BankCardRepository(host, user, password, db_name)
    expected_result = expected_result_for_find_by_uuid()
    result = func_test.find_by_uuid("fdd348f9-438c-4cd5-996d-e04de0019bd1")
    assert result[0] == expected_result
