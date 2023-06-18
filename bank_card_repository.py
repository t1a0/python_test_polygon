# Імпорт необхідних модулів та класів
from config import host, user, password, db_name
from bank_card import Card
from uuid import uuid4
import psycopg2


class BankCardRepository:
    def correct_date(self, date: str) -> str:
        first_day_of_month = "-01"
        return (
            date[-4:] + "-" + date[:2] + first_day_of_month
        )  # Перетворення формату дати

    def __init__(self, host: str, user: str, password: str, db_name: str):
        try:
            self.connection = psycopg2.connect(
                host=host, user=user, password=password, database=db_name
            )
            self.connection.autocommit = True
        except Exception as _ex:
            print(
                f"[Error] Error while connecting with PostgreSQL \n {_ex}"
            )  # Обробка помилки підключення

        self.cursor = self.connection.cursor()

        # Створення таблиці, якщо вона не існує
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS cards(
                                        card_number BIGINT PRIMARY KEY NOT NULL,
                                        card_exp_date DATE NOT NULL,
                                        card_cvv INT NOT NULL,
                                        card_issue_date DATE NOT NULL,
                                        card_uuid UUID NOT NULL,
                                        card_status VARCHAR(20));"""
        )

    def get(self, number: int) -> tuple:
        self.cursor.execute("SELECT * FROM cards WHERE card_number = %s", (number,))
        return self.cursor.fetchall()  # Отримання та повернення всіх рядків

    def save(self, Card):
        self.cursor.execute(
            "INSERT INTO cards VALUES(%s, %s, %s, %s, %s, %s)", Card.attributes()
        )  # Додавання даних до таблиці

    def update_status(self, Card):
        self.cursor.execute(
            "UPDATE cards SET card_status = %s WHERE card_number = %s",
            (Card.card_status, Card.card_number),
        )  # Оновлення статусу картки

    def find_by_exp_date(self, date: str) -> tuple:
        formatted_date = self.correct_date(date)
        self.cursor.execute(
            "SELECT * FROM cards WHERE card_exp_date = %s", (formatted_date,)
        )
        return (
            self.cursor.fetchall()
        )  # Отримання та повернення всіх рядків, що відповідають вказаній даті закінчення строку дії

    def find_by_issue_date(self, issue_date: str) -> tuple:
        self.cursor.execute(
            "SELECT * FROM cards WHERE card_issue_date = %s", (issue_date,)
        )
        return (
            self.cursor.fetchall()
        )  # Отримання та повернення всіх рядків, що відповідають вказаній даті видачі

    def find_by_uuid(self, uuid: str) -> tuple:
        self.cursor.execute("SELECT * FROM cards WHERE card_uuid = %s", (uuid,))
        return (
            self.cursor.fetchall()
        )  # Отримання та повернення всіх рядків, що відповідають вказаному uuid


if __name__ == "__main__":
    # Створення екземпляру BankCardRepository
    bank = BankCardRepository(host, user, password, db_name)

    # Створення об'єкту Card
    card1 = Card(
        1234_5678_9012_0000, "02/2022", 123, "2028-02-01", str(uuid4()), "active"
    )

    # Збереження картки в базі даних
    bank.save(card1)
    #  Отримання картки за номером
    print(bank.get(1234_5678_9012_0000))

    # Пошук карток за датою закінчення строку дії
    print(bank.find_by_exp_date("02/2022"))

    # Пошук карток за датою видачі
    print(bank.find_by_issue_date("2028-02-01"))

    # Оновлення статусу картки на "blocked"
    card1.card_status = "blocked"
    bank.update_status(card1)
    print(bank.get(1234_5678_9012_0000))

    # Оновлення статусу картки на "active", видає помилку через неможливість зміни статусу блокованної картки
    card1.card_status = "active"
    bank.update_status(card1)
    print(bank.get(1234_5678_9012_0000))

    # Пошук карток за UUID
    print(bank.find_by_uuid("b88603d9-91f6-4e7b-a088-d746e75e07f1"))
