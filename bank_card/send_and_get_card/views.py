import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpRequest

from send_and_get_card.models import BankCard


class BankCardView(View):

    def get(self, request: HttpRequest):
        card = BankCard.objects.get(number=request.GET['number'])

        return JsonResponse({'card': {'number': card.number,
                                      'exp_date': card.exp_date,
                                      'cvv': card.cvv,
                                      'issue_date': card.issue_date,
                                      'uuid': card.uuid,
                                      'status': card.status}})

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        card = BankCard(number=data['number'], exp_date=data['exp_date'], cvv=data['cvv'], issue_date=data['issue_date'])
        card.save()

        return JsonResponse({'card': {'number': card.number,
                                      'exp_date': card.exp_date,
                                      'cvv': card.cvv,
                                      'issue_date': card.issue_date,
                                      'uuid': card.uuid,
                                      'status': card.status}})
