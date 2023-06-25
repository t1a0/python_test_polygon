from flask import Flask, render_template, request
from config import host, user, password, db_name
from bank_card import Card
from bank_card_repository import BankCardRepository
from uuid import uuid4

app = Flask(__name__)


def check_number(number: str) -> bool:
    number = number.replace("-", "")
    if len(number) == 16 and number.isdigit():
        return False
    else:
        return True


def check_exp_date(exp_date: str) -> bool:
    backslash = exp_date[2]
    exp_date = exp_date.replace("/", "")
    if len(exp_date) == 6 and backslash == "/" and 1 <= int(exp_date[0:2]) <= 12:
        return False
    else:
        return True


def check_cvv(cvv: str) -> bool:
    if len(cvv) == 3 and cvv.isdigit():
        return False
    else:
        return True


def check_issue_date(date) -> bool:
    date = date.replace("-", "")
    if (
        len(date) == 8
        and date.isdigit()
        and 1 <= int(date[4:6]) <= 12
        and 1 <= int(date[6:]) <= 31
    ):
        return False
    else:
        return True


@app.route("/")
def main_page():
    return render_template("main_page.html", title="Головна сторінка")


@app.route("/create", methods=["GET", "POST"])
def create():
    error = ""
    success = ""
    repository = BankCardRepository(host, user, password, db_name)
    if request.method == "POST":
        if check_number(number := request.form["number"]):
            error = "Невірний номер !"
        elif check_exp_date(exp_date := request.form["exp_date"]):
            error = "Невірна дата кінцевого строку дії !"
        elif check_cvv(cvv := request.form["cvv"]):
            error = "Невірний cvv !"
        elif check_issue_date(issue_date := request.form["issue_date"]):
            error = "Невірна дата випуску !"
        else:
            number = number.replace("-", "")
            card1 = Card(
                int(number), exp_date, int(cvv), issue_date, str(uuid4()), "new"
            )
            try:
                repository.save(card1)
                success = "Додано нову банківську картку!"
            except:
                error = "Така картка вже існує!"
            finally:
                repository.disconnect()
    else:
        pass

    return render_template(
        "сreate.html", title="Створення картки", error=error, success=success
    )


@app.route("/check", methods=["GET", "POST"])
def check():
    error = ""
    result = ""
    if request.method == "POST":
        if check_number(number := request.form["number"]):
            error = "Невірний номер !"
        else:
            number = number.replace("-", "")
            repository = BankCardRepository(host, user, password, db_name)
            result = repository.get(int(number))
            repository.disconnect()
    return render_template("check.html", title="Пошук", error=error, result=result)


if __name__ == "__main__":
    app.run(debug=True)
