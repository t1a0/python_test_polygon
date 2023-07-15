from django.template.loader import render_to_string
from django.test import TestCase
from send_and_get_card.models import BankCard
from django.urls import reverse
import json
import uuid
from datetime import datetime


class CardsTest(TestCase):
    def test_get_card(self):
        create_card = BankCard(number=1111222233334444, exp_date="2077-01-01", cvv=456)
        create_card.save()

        card = BankCard.objects.filter(number=1111222233334444).first()

        url = reverse("show_card") + "?number=1111222233334444"

        response = self.client.get(url)

        actual_template = "show.html"
        data = {"title": "Пошук картки", "card": card}

        expected_result = render_to_string(actual_template, data)

        self.assertEquals(expected_result, response.content.decode("utf-8"))

    def test_post_card(self):
        data = {
            "number": 1111222233334444,
            "exp_date": "2077-01-01",
            "cvv": 123,
        }

        url = reverse("create_card")

        response = self.client.post(url, data=data)

        actual_template = "create.html"
        context = {"title": "Створення картки", "check": False}

        expected_result = render_to_string(actual_template, context)

        card = BankCard.objects.filter(number=1111222233334444).first()

        expect_data = {
            "number": 1111222233334444,
            "exp_date": "2077-01-01",
            "cvv": 123,
            "issue_date": str(datetime.now().date()),
            "uuid": True,
            "status": "new",
        }

        # then
        self.assertContains(response, "Картка додана.")
        self.assertEquals(
            expect_data,
            {
                "number": card.number,
                "exp_date": str(card.exp_date),
                "cvv": card.cvv,
                "issue_date": str(card.issue_date),
                "uuid": self.is_valid_uuid(str(card.uuid)),
                "status": card.status,
            },
        )

    def test_is_valid_false(self):
        card = BankCard(
            number=1111222233334443,
            exp_date="2025-01-01",
            cvv=123,
            issue_date="2000-01-01",
        )
        result = card.is_valid()
        self.assertEquals(result, False)

    def test_is_valid_true(self):
        # Create a card with a valid number
        card = BankCard(
            number=4003600000000014,
            exp_date="2025-01-01",
            cvv=123,
            issue_date="2000-01-01",
        )

        # Check if the card is valid
        result = card.is_valid()

        # Verify that the card is valid
        self.assertEquals(result, True)

    def is_valid_uuid(self, check_uuid: str):
        try:
            uuid_obj = uuid.UUID(check_uuid)
            is_valid_uuid = True
        except ValueError:
            is_valid_uuid = False
        return is_valid_uuid
