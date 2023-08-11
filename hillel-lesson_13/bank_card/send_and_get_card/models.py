from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Status(models.Model):
    status = models.CharField(max_length=25)

    def __str__(self):
        return self.status

class BankCard(models.Model):

    number = models.BigIntegerField(primary_key=True)
    name = models.CharField(null=True, max_length=255)
    exp_date = models.DateField()
    cvv = models.IntegerField()
    issue_date = models.DateField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid4, editable=False)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def is_valid(self):
        number_str = str(self.number)
        range1 = number_str[0:15:2]
        range2 = number_str[1:15:2] + '0'
        summ = sum((int(i) * 2) % 9 + int(j) for i, j in zip(range1, range2))
        return (summ + int(number_str[-1])) % 10 == 0
