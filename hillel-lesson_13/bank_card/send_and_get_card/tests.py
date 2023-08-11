from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse

from .models import BankCard, Status
from .serializer import CardSerializer

class CardsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Common test data setup
        cls.user = User.objects.create_user('test', password='test')
        cls.url = reverse('card-list')

        # Add status to the database
        for s_id, stat in [(1, 'active'), (2, 'blocked'), (3, 'freezed')]:
            status = Status(s_id, stat)
            status.save()

    def create_card_data(self):
        return {
            "number": 1111_1111_1111_1111,
            "exp_date": "2077-01-01",
            "cvv": 111
        }

    def test_api_list(self):
        card = BankCard.objects.create(owner=self.user, number=1111_1111_1111_1111,
                                       exp_date='2077-01-01', cvv=111)

        expected_result = [
            {
                "number": card.number,
                "name": card.name,
                "exp_date": card.exp_date,
                "cvv": card.cvv,
                "issue_date": str(card.issue_date),
                "uuid": str(card.uuid),
                "status": card.status.id
            }
        ]

        self.client.login(username=self.user.username, password='test')
        response = self.client.get(self.url).json()

        # Test with another user
        user2 = User.objects.create_user('test2', password='test2')
        self.client.login(username=user2.username, password='test2')
        response2 = self.client.get(self.url).json()
        expected_result2 = {'error': 'You don`t have any cards'}

        self.assertEqual(response, expected_result)
        self.assertEqual(response2, expected_result2)

    def test_api_create(self):
        self.client.login(username=self.user.username, password='test')
        data = self.create_card_data()
        response = self.client.post(self.url, data=data).json()

        card = BankCard.objects.filter(number=data['number']).first()
        expected_result = CardSerializer(card).data

        self.assertEqual(response, expected_result)

        # Test with anonymous user
        self.client.force_authenticate(user=None)
        response2 = self.client.post(self.url, data=data).json()
        expected_result2 = {
            "detail": "Authentication credentials were not provided."
        }

        self.assertEqual(response2, expected_result2)

    def test_api_detail(self):
        card = BankCard.objects.create(owner=self.user, number=1111_1111_1111_1111,
                                       exp_date='2077-01-01', cvv=111)

        url = reverse('card-detail', args=[card.number])
        expected_result = {
            "number": card.number,
            "name": card.name,
            "exp_date": card.exp_date,
            "cvv": card.cvv,
            "issue_date": str(card.issue_date),
            "uuid": str(card.uuid),
            "status": card.status.id
        }

        self.client.login(username=self.user.username, password='test')
        response = self.client.get(url).json()

        # Test with another user
        user2 = User.objects.create_user('test2', password='test2')
        self.client.login(username=user2.username, password='test2')
        response2 = self.client.get(url).json()
        expected_result2 = {
            "detail": "You do not have permission to perform this action."
        }

        self.assertEqual(response, expected_result)
        self.assertEqual(response2, expected_result2)

    def test_api_update(self):
        card = BankCard.objects.create(owner=self.user, number=1111_1111_1111_1111,
                                       exp_date='2077-01-01', cvv=111)

        url = reverse('card-detail', args=[card.number])
        data = {
            "name": "user",
            "cvv": 121
        }

        expected_result = {
            "number": card.number,
            "name": data['name'],
            "exp_date": card.exp_date,
            "cvv": data['cvv'],
            "issue_date": str(card.issue_date),
            "uuid": str(card.uuid),
            "status": card.status.id
        }

        self.client.login(username=self.user.username, password='test')
        response = self.client.patch(url, data=data).json()

        card = BankCard.objects.filter(number=1111_1111_1111_1111).first()
        result = CardSerializer(card).data

        # Test with another user
        user2 = User.objects.create_user('test2', password='test2')
        self.client.login(username=user2.username, password='test2')
        response2 = self.client.patch(url, data=data).json()
        expected_result2 = {
            "detail": "You do not have permission to perform this action."
        }

        self.assertEqual(result, expected_result)
        self.assertEqual(response2, expected_result2)

    def test_api_freeze(self):
        card = BankCard.objects.create(owner=self.user, number=1111_1111_1111_1111,
                                       exp_date='2077-01-01', cvv=111)

        url = reverse('card-freeze', args=[card.number])

        expected_result = {
            "number": card.number,
            "name": card.name,
            "exp_date": card.exp_date,
            "cvv": card.cvv,
            "issue_date": str(card.issue_date),
            "uuid": str(card.uuid),
            "status": 3
        }

        self.client.login(username=self.user.username, password='test')
        response = self.client.get(url).json()

        card = BankCard.objects.filter(number=1111_1111_1111_1111).first()
        result = CardSerializer(card).data

        # Test with another user
        user2 = User.objects.create_user('test2', password='test2')
        self.client.login(username=user2.username, password='test2')
        response2 = self.client.get(url).json()
        expected_result2 = {'error': 'It`s not your card'}

        self.assertEqual(result, expected_result)
        self.assertEqual(response2, expected_result2)

    def test_api_reactivate(self):
        card = BankCard.objects.create(owner=self.user, number=1111_1111_1111_1111,
                                       exp_date='2077-01-01', cvv=111)

        url = reverse('card-reactivate', args=[card.number])

        expected_result = {
            "number": card.number,
            "name": card.name,
            "exp_date": card.exp_date,
            "cvv": card.cvv,
            "issue_date": str(card.issue_date),
            "uuid": str(card.uuid),
            "status": 2
        }

        self.client.login(username=self.user.username, password='test')
        response = self.client.get(url).json()

        card = BankCard.objects.filter(number=1111_1111_1111_1111).first()
        result = CardSerializer(card).data

        # Test with another user
        user2 = User.objects.create_user('test2', password='test2')
        self.client.login(username=user2.username, password='test2')
        response2 = self.client.get(url).json()
        expected_result2 = {'error': "It`s not your card"}

        self.assertEqual(result, expected_result)
        self.assertEqual(response2, expected_result2)
