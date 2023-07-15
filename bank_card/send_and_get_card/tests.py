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

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show.html")
        self.assertContains(response, "Пошук картки")
        self.assertContains(response, str(card.number))
        self.assertContains(response, str(card.cvv))
        self.assertEqual(response.context["card"].exp_date, card.exp_date)

    def test_post_card(self):
        data = {
            "number": 1111222233334444,
            "exp_date": "2077-01-01",
            "cvv": 123,
        }

        url = reverse("create_card")

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create.html")
        self.assertContains(response, "Створення картки")
        self.assertContains(response, "Картка додана.")

        card = BankCard.objects.filter(number=1111222233334444).first()

        self.assertEqual(card.number, 1111222233334444)
        self.assertEqual(str(card.exp_date), "2077-01-01")
        self.assertEqual(card.cvv, 123)
        self.assertEqual(str(card.issue_date), str(datetime.now().date()))
        self.assertTrue(self.is_valid_uuid(str(card.uuid)))
        self.assertEqual(card.status, "new")

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
