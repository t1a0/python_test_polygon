from django.test import TestCase
from send_and_get_card.models import BankCard
from django.urls import reverse
import json


class CardsTest(TestCase):

    def test_get_card(self):
        # Create a card
        card = BankCard(number=1111222233334444, exp_date='2020-01-01', cvv=123, issue_date = '2000-01-01')
        card.save()
        url = reverse('bank_card') + '?number=1111222233334444'

        # Send a GET request to retrieve the card
        response = self.client.get(url).json()

        # Verify the response matches the card details
        expected_response = {
            'card': {
                'number': card.number,
                'exp_date': str(card.exp_date),
                'cvv': card.cvv,
                'issue_date': str(card.issue_date),
                'uuid': str(card.uuid),
                'status': card.status
            }
        }
        self.assertEquals(response, expected_response)

    def test_post_card(self):
        # Create a unique card
        data = json.dumps({
            "number": 1111222233334455,
            "exp_date": "2020-01-01",
            "cvv": 123,
            "issue_date": "2000-01-01"
        })
        url = reverse('bank_card')

        # Send a POST request to create the card
        response = self.client.post(url, data=data, content_type='application/json')

        # Retrieve the created card
        card = BankCard.objects.filter(number=1111222233334455).first()

        # Verify the response and card details match
        expected_response = {
            'card': {
                'number': card.number,
                'exp_date': str(card.exp_date),
                'cvv': card.cvv,
                'issue_date': str(card.issue_date),
                'uuid': str(card.uuid),
                'status': card.status
            }
        }

        response_data = response.json()

        self.assertEquals(response_data, expected_response)

    def test_is_valid_false(self):
        card = BankCard(number=1111222233334443, exp_date='2025-01-01', cvv=123, issue_date= "2000-01-01")
        result = card.is_valid()
        self.assertEquals(result, False)
