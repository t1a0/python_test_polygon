from django.db import models
from uuid import uuid4


class BankCard(models.Model):

    number = models.BigIntegerField(primary_key=True)
    exp_date = models.DateField()
    cvv = models.IntegerField()
    issue_date = models.DateField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid4, editable=False)
    status = models.CharField(max_length=50, default='new')


    def is_valid(self):
        number_str = str(self.number)
        range1 = number_str[0:15:2]
        range2 = number_str[1:15:2] + '0'
        summ = sum((int(i) * 2) % 9 + int(j) for i, j in zip(range1, range2))
        return (summ + int(number_str[-1])) % 10 == 0
